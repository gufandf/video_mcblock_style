import cv2
import os
import json

blockToColor = {}

def get_img_color(Path:str):
    image = cv2.imread(Path)
    average_color_per_channel = cv2.mean(image)
    average_color = (int(average_color_per_channel[2]), int(average_color_per_channel[1]), int(average_color_per_channel[0]))
    return average_color

for files in os.walk("./block/"):
    for file in files[2]:
        if ".png" == file[-4:]:
            color = get_img_color(f"./block/{file}")
            print(file,color)
            blockToColor[file[:-4]] = color

f = open("./block2color.json","w",encoding="UTF-8")
f.write(json.dumps(blockToColor))