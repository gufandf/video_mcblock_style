from PIL import Image
import os
from search import *
from tqdm import tqdm
import time
import subprocess
import cv2
import shutil
from pathlib import Path
from multiprocessing import Process, Pool


def del_file(path):
    for elm in Path(path).glob("*"):
        # print(elm)
        elm.unlink() if elm.is_file() else shutil.rmtree(elm)


for i in ["temp", "frame", "video"]:
    try:
        os.makedirs(i)
    except FileExistsError:
        pass


def transPhoto(input_path: str, output_path: str):
    """
    转换单张图片
    """
    im = Image.open(input_path)
    im = im.convert("RGBA")
    re = Image.new("RGB", size=(im.size[0] * 16, im.size[1] * 16))

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            # block = get_block(im.getpixel((i,j)))
            block = get_block_fast(im.getpixel((i, j)))
            blockim = Image.open(f"./block/{block}.png").copy().convert("RGBA")
            re.paste(blockim, [i * 16, j * 16])

    re.save(f"{output_path}.", output_path.split(".")[-1])
    re.close()
    im.close()
    blockim.close()
    print("已完成："+input_path)


def transVideo(input_path: str, output_path: str):
    """
    转换视频
    """
    print("[TRANS MAIN]正在拆分帧")
    videoCapture = cv2.VideoCapture(input_path)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    subprocess.call(
        f'ffmpeg -loglevel quiet -i "{input_path}" -vf "scale=iw/16:ih/16" "./temp/frame%06d.png"'
    )

    MAX_THREADS = 15
    pool = Pool(processes=MAX_THREADS)

    print("[TRANS MAIN]分配线程")
    for path, floder, files in os.walk("./temp/"):
        for fileName in files:
            file_path = path + fileName
            pool.apply_async(func=transPhoto, args=(file_path, "./frame/" + fileName))

    print("[TRANS MAIN]等待所有线程完成...")
    pool.close()
    pool.join()

    print("[TRANS MAIN]正在合并帧")
    subprocess.call(
        f'ffmpeg -loglevel quiet -r {fps} -f image2 -i ./frame/frame%06d.png -i "{input_path}" -c:v copy -map 0:v -map 1:a -vcodec libx264 -pix_fmt yuv420p "{output_path}"'
    )
    print("[TRANS MAIN]回收空间中")
    del_file("./temp/")
    del_file("./frame/")
    print("[TRANS MAIN]转码成功")

if __name__ == "__main__":
    transVideo(input("原视频："), input("输出位置："))
