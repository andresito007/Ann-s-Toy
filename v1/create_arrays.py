import numpy as np
from math import factorial as fac

WORDS = ['真的','打響', '紅茶', '社團', '高興', '開', '熱', '套', '冷', '黑',
         '就', '苦', '好', '你', '他', '我', '乾淨', '討厭', '聊天', '喜歡', 
         '漂亮', '台北', '貓', '狗', '孩子', '杯子', '大', '小', '另', '餓', 
         '輕', '使用', '間接', '無聊', '強', '好奇', '花', '若', '如果', '被動',
         '孤單', '恐怖', '直接', '耐心', '愉快', '嚴格', '主動', '正式', '努力', '激烈']

def SumElements(numObjs):
    suma = 0

    for i in range(numObjs, 0, -1):
        suma += i 

    return suma

def CreateArrays():
    numObjs = 9

    # print(SumElements(numObjs), len(WORDS))
    if len(WORDS) < SumElements(numObjs):
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

        front = WORDS[init:numAux]      
        # print(front)  
        array.extend(front)
        array.extend(back)

        answer.append(array)

        print(i, array)
        # print("-------------------------")

        init = numAux 
        numAux = numObjs - i - 1
        numAux = init + numAux

    return answer


def Main():
    arrays = CreateArrays()
   

if __name__ == "__main__":
    Main()