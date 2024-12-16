import json


f = open("./block2color.json","r",encoding="UTF-8")
blockToColor = json.loads(f.read())
f = open("./color2block.json","r",encoding="UTF-8")
color2block = json.loads(f.read())
f.close()


def get_color(block:str):
    return blockToColor[block]

def get_block(color:tuple):
    min = 196608
    target_block = ""
    for key in blockToColor:
        d = (pow(blockToColor[key][0]-color[0],2)+pow(blockToColor[key][1]-color[1],2)+pow(blockToColor[key][2]-color[2],2))
        if d < min:
            min = d
            target_block = key
    return target_block

def get_block_fast(color:tuple):
    color = (int(color[0]/16)*16,int(color[1]/16)*16,int(color[2]/16)*16)
    return color2block[str(color)]
# print(get_block((0,0,0)))
