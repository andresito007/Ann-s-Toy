from PIL import ImageFont, ImageDraw, Image
from typing import Tuple
import pandas as pd
import numpy as np
import shutil
import cv2
import os 

TEXT_SIZE = 110
NUM_POINTS = 7
DIM = 0
R1, R2, R3 = 0, 0, 0

def LoadWords():
    file = 'words.txt'
    words = pd.read_csv(file, header=None)
    return words[0].tolist()

def SumElements(numObjs):
    suma = 0

    for i in range(numObjs, 0, -1):
        suma += i 

    return suma

def CreateArrays(words):
    numObjs = 7

    # print(SumElements(numObjs), len(WORDS))
    if len(words) < SumElements(numObjs):
        print("Not enought words")
        return None

    init = 0
    numAux = numObjs

    answer = []
    for i in range(numObjs+1):
        array = []
        back = []

        long = len(answer)
        for j, elem in enumerate(answer):
            first = elem[long - j - 1]
            back.append(first)

        front = words[init:numAux]      
        # print(front)  
        array.extend(front)
        array.extend(back)

        answer.append(array)

        # print(i, array)
        # print("-------------------------")

        init = numAux 
        numAux = numObjs - i - 1
        numAux = init + numAux

    return answer

def CreateEmptyImage():
    h, w, c = 800, 800, 3
    return  255*np.ones(shape=(h, w, c), dtype='uint8')

def CreateCircles(arrayCircles):
    img = CreateEmptyImage()

    imgs = []
    for i, array in enumerate(arrayCircles):
        array = np.random.permutation(array)
        img1 = ScatterWords(img, array)
        imgs.append(img1)

    return imgs

def init_parameters(fun, **init_dict):
    def job(*args, **option):
        option.update(init_dict)

        return fun(*args, **option)

    return job

def cv2_img_add_text(img, text, left_corner: Tuple[int, int], text_rgb_color=(255, 0, 0), text_size=24, font='mingliu.ttc', **option):
    pil_img = img

    if isinstance(pil_img, np.ndarray):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(pil_img)
    font_text = ImageFont.truetype(font=font, size=text_size, encoding=option.get('encoding', 'utf-8'))
    draw.text(left_corner, text, text_rgb_color, font=font_text)
    cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)

    if option.get('replace'):
        img[:] = cv2_img[:]
    
        return None

    return cv2_img

def ScatterWords(image, arrayCircle):
    global DIM, R1, R2, R3
    
    img = image.copy()
    h, w, c = img.shape

    center = (w//2, h//2)
    DIM = int(w)
    R1, R2, R3 = int(DIM/16), int(DIM/2)-30, int(DIM/8)

    cv2.circle(img, center, h//2, [0,0,0], 2)
    cv2.circle(img, center, 2, [0,0,0], -1)

    colors = np.random.randint(0, 255, (7, 3)).tolist()
    positions = DefinePositions()
    positions = positions - R3
    # [cv2.circle(img, (int(positions[i,0]), int(positions[i,1])), R3, 0, 1) for i in range(NUM_POINTS)]
    positions = positions.tolist()

    # pos = POS + np.random.randint(-20, 20, (7,2))

    for i, word in enumerate(arrayCircle):
        draw_text = init_parameters(cv2_img_add_text, text_size=TEXT_SIZE, text_rgb_color=tuple(colors[i]), font='kaiu.ttf', replace=True)
        draw_text(img, word, tuple(positions[i]))

    return img
    
def CheckLength(imgs):
    if (len(imgs) % 2) != 0:
        imgs.append(CreateEmptyImage())
        CheckLength(imgs)

def SaveImages(imgs, param):
    CheckLength(imgs)
    
    path = 'img'
    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

    if param == 0:
        for k, img in enumerate(imgs):
            cv2.imwrite(r'img\img{}.png'.format(format(k, "02")), img)

    elif param == 1:
        lines = []
        for i in range(0, len(imgs), 2):
            lines.append(np.hstack((imgs[i], imgs[i+1])))

        for k, i in enumerate(range(0, len(lines), 2)):
            aux = np.vstack((lines[i], lines[i+1]))
    
            cv2.imwrite(r'img\img{}.png'.format(format(k, "02")), aux)
            # cv2.imshow("img{}".format(i), aux)
            # cv2.moveWindow("img{}".format(i), 0, 0)
    
    cv2.waitKey(0)

def CreatePosition():
    global DIM

    return np.random.randint(0, DIM, 2)

def CheckDistanceCenterPoint(p1):
    dPC = np.sqrt(np.power(DIM/2 - p1[0], 2) + np.power(DIM/2 - p1[1], 2)) + R3
    C1 = R1 < dPC < R2

    return C1

def CheckFirstPoint(p1):
    C1 = CheckDistanceCenterPoint(p1)

    if C1:
        return p1
    else:
        return CheckFirstPoint(CreatePosition())

def CheckNewPoint(p1, points):
    tries = 0
    flag = False
    while(True):
        C1 = CheckDistanceCenterPoint(p1)  
        distances = np.sqrt(np.power(p1[0] - points[:,0], 2) + np.power(p1[1] - points[:,1], 2))
        results = distances > 2*R3
        C2 = results.all() == True
        C3 = tries == 1000

        if C1 and C2:
            break
        else:
            p1 = CreatePosition()
            tries = tries+1

        if C3:
            flag = True
            break

    return p1, flag

def DefinePositions():
    positions = np.zeros(shape=(NUM_POINTS,2))
    for i in range(NUM_POINTS):
        ranPos = CreatePosition()

        if i==0:
            positions[i,:] = CheckFirstPoint(ranPos)
        else:
            positions[i,:], flag = CheckNewPoint(ranPos, positions[:i,:])
            
            if flag:
                positions = DefinePositions()
                break

        print('|'*i)

    return positions

def Main():
    words = LoadWords()
    arrays = CreateArrays(words)
    imgs = CreateCircles(arrays)
    SaveImages(imgs, 0)

if __name__ == "__main__":
    Main()
    print('Process finished')