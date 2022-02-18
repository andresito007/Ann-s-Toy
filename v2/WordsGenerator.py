from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pandas as pd

def CheckShape(shape):
    HorTiles, VerTiles = shape[0], shape[1]

    # Check inputs
    if type(HorTiles) != int:
        HorTiles = 3
    else:
        if HorTiles > 10:
            HorTiles = 10
        elif HorTiles < 1:
            HorTiles = 1

    if type(VerTiles) != int:
        VerTiles = 6
    else:
        if VerTiles > 10:
            VerTiles = 10
        elif VerTiles < 1:
            VerTiles = 1
    
    return (HorTiles, VerTiles)

def DrawGrid(shape=(3, 3), grid=False):
    # initial setup
    horizontal=100*shape[0]
    vertical=100*shape[1]

    im = Image.new("RGB", (horizontal+1, vertical+1), "white")
    d = ImageDraw.Draw(im)

    # contour
    d.line(((0, 0), (horizontal, 0)), "black", width=3)
    d.line(((horizontal, 0), (horizontal, vertical)), "black", width=3)
    d.line(((horizontal, vertical), (0, vertical)), "black", width=3)
    d.line(((0, vertical), (0, 0)), "black", width=3)
    
    if grid:
        # grid horizontal 
        res = int(vertical / 100)
        for i in range(1, res):
            d.line(((0, 100*i), (horizontal, 100*i)), "gray")

        # grid vertical
        res = int(horizontal / 100)
        for i in range(1, res):
            d.line(((100*i, 0), (100*i, vertical)), "gray")

    return im

def ChooseTiles(shape, numObjs):
    numTiles = shape[0]*shape[1]

    TilesName =  np.arange(numTiles)
    opts = np.sort(np.random.choice(TilesName, numObjs, replace=False))
    TilesDist, cont = [], 0
    for i in range(shape[1]):
        auxTiles = []
        for j in range(shape[0]):
            if cont in opts:
                auxTiles.append(1)
            else:
                auxTiles.append(0)
            cont += 1
        TilesDist.append(auxTiles)
    
    return TilesDist

def ScatterObjects(objs, tilesDist, im):
    cont = 0
    for i, row in enumerate(tilesDist):
        for j, column in enumerate(row):
            if (column == 1):
                if objs[cont][0] == 1:
                    pos = (100*j+50, 100*i+65)
                else:
                    img = objs[cont][1] 
                    width, height = img.size
                    if width > height:
                        vPos = int((100 - height) / 2)
                        pos = (100*j+2, 100*i+vPos)
                    else:
                        hPos = int((100 - width) / 2)
                        pos = (100*j+hPos, 100*i+2)

                objs[cont].append(pos)
            
                color = tuple(np.random.randint(0, 255, (1, 3))[0])
                objs[cont].append(color)
                cont += 1

    d = ImageDraw.Draw(im)
    font = ImageFont.truetype("kaiu.ttf", 48)
    for object in objs:
        if object[0] == 1:
            d.text(object[2], object[1], fill=object[3], anchor="ms", font=font)
        else:
            im.paste(object[1], object[2])

def ReadObjs(shape, numObjects, filename="objects.txt"):
    maxObjects = shape[0]*shape[1]
    if numObjects > maxObjects:
        numObjects = maxObjects

    words = pd.read_csv(filename, header=None)
    words = words[0].tolist()

    numSets = int(len(words) // numObjects) + 1
    init, end = 0, numObjects
    listWords = []
    for i in range(numSets):
        auxWords = words[init:end]
        if len(auxWords) == 0:
            continue
        
        listWords.append(auxWords)
        init = end
        end = end + numObjects

    listObjects = []
    for words in listWords:
        objects = []
        for word in words:
            if (".png" in word) or (".jpg" in word):
                im = Image.open(word)
                width, height = im.size
                if width > height:
                    newHeight = int((95 / width) * height)
                    newSize = (95, newHeight)
                else:
                    newWidth = int((95 / height) * width)
                    newSize = (newWidth, 95)
                newIm = im.resize(newSize)
                objects.append([0, newIm])
            else:
                objects.append([1, word])
        listObjects.append(objects)

    return listObjects
