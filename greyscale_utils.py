import cv2
from statistics import mode
import numpy as np

def posgradient(p, mc, gradient):
    if gradient == 0:
        return False
    if p == mc + gradient or p == mc - gradient:
        return True
    else:
        gradient = gradient - 1
        posgradient(p, mc, gradient)


def neggradient(p, mc, gradient):
    if gradient == 0:
        return False
    if p != mc - gradient or p != mc + gradient:
        return True
    else:
        gradient = gradient - 1
        neggradient(p, mc, gradient)


def mostcommon(matrix):
    mode_per_row = []
    for row in matrix:
        # print("row:", row)
        mc = mode(row)
        mode_per_row.append(mc)
    print("Mode Per row:", mode_per_row)
    print("Mode of all rows:", mode(mode_per_row))
    return mode(mode_per_row)


# loop every row and find an entry and exit point
# for clusters of data that are not equal to the mode(most common)
# change row values to ignore all points that are not edges( entry and exit points where the data changes in the row)
# finally return a changed matrix
# *** Shape function is designed for grayscale images*** ###
def shape(matrix, mode):
    newm = []
    gradient = 5
    for row in matrix:
        i = 0  # iterator
        newr = []  # new matrix
        mc = mode  # (row)
        entry = 0
        for p in row:
            if (p == mc or p == mc + 1 or p == mc - 1):  #  posgradient(p, mc, gradient)
                # set exit point
                if entry != 0:
                    entry = 0
                    newr.append(100)
                else:
                    newr.append(0)
            elif (p != mc or p != mc + 1 or p != mc - 1):  # or  neggradient(p, mc, gradient)
                # set entry point
                if (entry == 0):
                    entry = 1
                    newr.append(100)
                # continue after entry
                else:
                    newr.append(0)
            else:
                newr.append(0)
        newm.append(newr)

    print("Shape length dimensions:", len(newm))
    print("Shape width dimensions:"), len(newm[0])
    np.set_printoptions(threshold=np.inf, linewidth=1000)
    new = np.matrix(newm)
    # print("Shape matrix:\n", new)
    return new


def process(matrix):
    # length
    ln = len(matrix)
    # Mode of matrix(mode of all row modes)
    print("\n## Grey image ###")
    mode = mostcommon(matrix)

    # shape
    # reference to local background depends on local or global mode.
    # Try to do blocks of modes for 3x3 or 5x5 pixel blocks for more detailed outlines
    print("\n### Shape function ###")
    # mode = mostcommon()
    shap = shape(matrix, mode)

    # Contour
    #print("\n## OpenCV contour tool##  ")
    ret, thresh = cv2.threshold(matrix, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(matrix, contours, -1, (0,255,0), 3)
    cv2.imshow("contour", matrix)


    # Display
    # cv2.imshow('Frames', frame)
    # plt.matshow(shap)
    # plt.show()
    return shap