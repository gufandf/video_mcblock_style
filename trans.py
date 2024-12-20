from PIL import Image
import os
from search import *
from tqdm import tqdm
import time
import subprocess
import cv2
import threading
import shutil
from pathlib import Path


def del_file(path):
    for elm in Path(path).glob('*'):
        # print(elm)
        elm.unlink() if elm.is_file() else shutil.rmtree(elm)

for i in ["temp","frame","video"]:
    try:
        os.makedirs(i)
    except FileExistsError:
        pass

def transPhoto(input_path:str,output_path:str):
    im = Image.open(input_path)
    im = im.convert("RGBA")
    re = Image.new("RGB",size=(im.size[0]*16,im.size[1]*16))

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            # block = get_block(im.getpixel((i,j)))
            block = get_block_fast(im.getpixel((i,j)))
            blockim = Image.open(f"./block/{block}.png").copy().convert("RGBA")
            re.paste(blockim,[i*16,j*16])


    re.save(f"{output_path}.", output_path.split(".")[-1])
    re.close()
    im.close()
    blockim.close()

def transVideo(input_path:str,output_path:str):
    print("[TRANS MAIN]正在拆分帧")
    videoCapture=cv2.VideoCapture(input_path)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    subprocess.call(f"ffmpeg -loglevel quiet -i \"{input_path}\" -vf \"scale=iw/16:ih/16\" \"./temp/frame%06d.png\"")
    
    MAX_THREADS = 15
    semaphore = threading.Semaphore(MAX_THREADS)

    def worker(semaphore,arg1,arg2):
        with semaphore:
            transPhoto(arg1,arg2)

    threads = []

    print("[TRANS MAIN]分配线程")
    for path,floder,files in os.walk("./temp/"):
        for fileName in files:
            file_path = path+fileName
            thread = threading.Thread(target=worker, args=(semaphore,file_path,"./frame/"+fileName))
            threads.append(thread)
            thread.start()

    print("[TRANS MAIN]等待所有线程完成...")
    for thread in tqdm(threads):
        thread.join()
    
    subprocess.call(f"ffmpeg -loglevel quiet -r {fps} -f image2 -i ./frame/frame%06d.png -i \"{input_path}\" -c:v copy -map 0:v -map 1:a -vcodec libx264 -pix_fmt yuv420p \"{output_path}\"")
    print("[TRANS MAIN]回收空间中")
    del_file("./temp/")
    del_file("./frame/")
    print("[TRANS MAIN]转码成功")

transVideo(input("原视频："),input("输出位置："))