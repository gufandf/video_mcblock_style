from search import *

color2block = {}

for r in range(16):
    for g in range(16):
        for b in range(16):
            color2block[str((r*16,g*16,b*16))] = get_block([r*16,g*16,b*16])

f = open("./color2block.json","w",encoding="UTF-8")
f.write(json.dumps(color2block))