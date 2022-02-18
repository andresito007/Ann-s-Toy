import numpy as np
import cv2

DIM = 480
R1, R2 = int(DIM/16), int(DIM/2)
R3 = int(DIM/8)
NUM_POINTS = 7

def CreatePosition():
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
                print('here')
                positions = DefinePositions()
                break

    return positions

def run():
    imgE = 255*np.ones(shape=(DIM, DIM))

    cv2.circle(imgE, (int(DIM/2), int(DIM/2)), R1, 0, 1)
    cv2.circle(imgE, (int(DIM/2), int(DIM/2)), R2, 0, 1)
    
    positions = DefinePositions()

    [cv2.circle(imgE, (int(positions[i,0]), int(positions[i,1])), R3, 0, 1) for i in range(NUM_POINTS)]

    cv2.imshow("img", imgE)

    cv2.waitKey(0)

if __name__ == "__main__":
    run()