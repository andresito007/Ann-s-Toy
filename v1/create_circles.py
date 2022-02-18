from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2

WORDS = ['真的','打響', '紅茶', '社團', '高興', '開', '熱', '套', '冷', '黑',
         '就', '苦', '好', '你', '他', '我', '乾淨', '討厭', '聊天', '喜歡', 
          '漂亮', '台北', '貓', '狗', '孩子', '杯子', '大', '小', '冷', '餓']

POS = [[150,150], [100, 350], [150,550], [350,350], [450,150], [550,350], [450,550]]

def RandomGenerator(words, wordsInCircle=5):

    arrayCircles = {}

    for i, word in enumerate(WORDS):
        if len(arrayCircles) == 0:
            newArrayWords = []
            newArrayWords.append(word)
            newArrayWords.append(words[-1])

            auxArraywords = words.copy()
            auxArraywords.pop(i)
            auxArraywords = np.random.choice(auxArraywords, wordsInCircle, replace=False)
            auxArraywords = auxArraywords.tolist()

            newArrayWords.extend(auxArraywords)
        else:
            newArrayWords = []
            newArrayWords.append(word)
            newArrayWords.append(words[i-1])

            auxArraywords = words.copy()
            auxArraywords.pop(i)
            auxArraywords = CheckWords(arrayCircles[i-1], auxArraywords)
            auxArraywords = np.random.choice(auxArraywords, wordsInCircle, replace=False)
            auxArraywords = auxArraywords.tolist()

            newArrayWords.extend(auxArraywords)

        newArrayWords = np.random.permutation(newArrayWords)
        # print(newArrayWords)
        arrayCircles[i] = newArrayWords

    return arrayCircles

def CheckWords(arrayWords, words):
    newArrayWords = []

    for word in words:
        if word not in arrayWords:
            newArrayWords.append(word)

    return newArrayWords

def CreateCircles(arrayCircles):
    h, w, c = 800, 800, 3

    img = 255*np.ones(shape=(h, w, c), dtype='uint8')


    arrayCircle1 = arrayCircles[0]
    arrayCircle2 = arrayCircles[1]

    img1 = ScatterWords(img, arrayCircle1)
    img2 = ScatterWords(img, arrayCircle2)

    cv2.imshow("img1", img1)
    cv2.moveWindow("img1", 0, 0)

    cv2.imshow("img2", img2)
    cv2.moveWindow("img2", w, 0)

    cv2.waitKey(0)


def ScatterWords(image, arrayCircle):
    img = image.copy()
    h, w, c = img.shape

    center = (w//2, h//2)
    color = [0,0,0]

    cv2.circle(img, center, h//2, color, 2)
    cv2.circle(img, center, 2, color, -1)

    # pos = np.random.randint(h//6, 5*h//6, (7, 2)).tolist()
    pos = POS + np.random.randint(-20, 20, (7,2))
    colors = np.random.randint(0, 255, (7, 3)).tolist()

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL 

    fontpath = "./simsun.ttc" 
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    # draw.text((50, 80),  "端午节就要到了。。。", font = font, fill = (255, 255, 255, 0))
    # img = np.array(img_pil)

    for i, word in enumerate(arrayCircle):
        font = ImageFont.truetype(fontpath, np.random.randint(80, 110, (1)))
        draw.text(pos[i],  '{}'.format(word), font = font, fill = tuple(colors[i]))
        img = np.array(img_pil)
        # cv2.putText(img, word, tuple(pos[i]), font, 1, colors[i], 2)
        
    return img
    
if __name__ == "__main__":
    arrayCircles = RandomGenerator(WORDS)
    CreateCircles(arrayCircles)
    

        

        



