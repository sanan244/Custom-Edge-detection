import numpy as np
import random

red = 0
green = 0
blue = 0
low = 0
high = 255


# takes in a list not numpy matrix
def flip_matrix(mat):
    newmat = []
    for row in mat:
        row.reverse()
        newmat.append(row)
    new = np.matrix(newmat)
    return new, newmat


# takes in a list not numpy matrix
def rotate_mat(mat):
    newmat = list(zip(*mat[::-1]))
    return newmat


def pixnum(r, g, b):
    bigtosmall = [2]
    bigtosmall.append(r)
    bigtosmall.append(g)
    bigtosmall.append(b)
    order = bigtosmall.sort()
    print("Order:", order)


# returns a matrix that replaces rgb values with rations or rgb to 255
# (n.nnnn%) on a scale of 0 to 1
def matrix_ratio(frame, decimals="6"):
    matrix = []
    dec_format = "{0:." + decimals + "f}"
    for row in frame:
        row_ratios = []
        for pixel in row:
            ratio = []
            for c in pixel:
                if c == 0:
                    ratio.append(0)
                    continue
                val = c / high
                ratio.append(float(dec_format.format(val)))
            row_ratios.append(ratio)
        matrix.append(row_ratios)
    # print("Dimensions Row ratio:", len(row_ratios), len(row_ratios[0]))
    print("Matrix:", len(matrix), len(matrix[0]))
    return matrix


# returns a contour matrix of 0's and 1's to draw on a plot(over original image)
# if one pixel color(rgb) is different enough from previous that constitutes a contour edge(i.e) boundary change
def compare_horzratios(mat, thresh=0.25):
    # matrix
    newmat = []
    current_ratio = [None, None, None]
    # set ratio to first pixel
    # print("Initial ratio: ", current_ratio)

    # start comparing pixels
    for row in mat:
        cont_pos = []
        r = mat.index(row)
        current_ratio[0] = mat[r][0][0]
        current_ratio[1] = mat[r][0][1]
        current_ratio[2] = mat[r][0][2]
        for pix in row:
            i = 0
            for r in pix:
                # if pixel is different than previous pixels
                if r > (current_ratio[i] + (current_ratio[i] * thresh)) or r < (
                        current_ratio[i] - (current_ratio[i] * thresh)):
                    current_ratio[0] = pix[0]
                    current_ratio[1] = pix[1]
                    current_ratio[2] = pix[2]
                    cont_pos.append(1)
                    break
                    # check_ratio[i] = r
                # if all pixels values are within range
                elif i == 2:
                    #avg_ratio =
                    cont_pos.append(0)
                    break
                i = i + 1
        # row.reverse()
        # print(cont_pos)
        newmat.append(cont_pos)
    np.set_printoptions(threshold=np.inf, linewidth=1000)
    new = np.matrix(newmat)
    # print(len(cont_pos))
    return new, newmat


# returns a contour matrix of 0's and 1's to draw on a plot(over original image)
# if one pixel color(rgb) is different enough from previous that constitutes a contour edge(i.e) boundary change
def compare_verti_ratios(mat, thresh=0.25):
    # matrix
    newmat = []
    # contour row positions
    #                  r     g     b
    current_ratio = [None, None, None]

    # start comparing pixels
    p = 0
    # columns
    while p < len(mat[0]):
        cont_pos = []
        current_ratio[0] = mat[0][p][0]
        current_ratio[1] = mat[0][p][1]
        current_ratio[2] = mat[0][p][2]
        i = 0
        # rows
        while i < len(mat):
            c = 0
            # r/g/b
            for r in mat[i][p]:
                # if pixel is different than previous pixels
                if r > (current_ratio[c] + (current_ratio[c] * thresh)) or r < (
                        current_ratio[c] - (current_ratio[c] * thresh)):
                    current_ratio[0] = mat[i][p][0]
                    current_ratio[1] = mat[i][p][1]
                    current_ratio[2] = mat[i][p][2]
                    cont_pos.append(1)
                    break
                    # check_ratio[i] = r                # if all pixels values are within range
                elif c == 2:
                    cont_pos.append(0)
                    break
                c = c + 1  # r/g/b
            i = i + 1  # pixel
        # print(cont_pos)
        newmat.append(cont_pos)
        p = p + 1  # column
    newmat = list(zip(*newmat[::-1]))
    # print("Newmat:\n", newmat)
    # print(len(newmat), len(newmat[0]))
    np.set_printoptions(threshold=np.inf, linewidth=1000)
    new = np.matrix(newmat)
    return new, newmat


# horizontal distance matrix
def hor_dist(mat):
    r = 0
    newmat = []
    for row in mat:
        t = 0
        newrow = []
        for p in row:
            dist = 0
            if t == 0 or t == len(mat[0]) - 1:
                newrow.append(0)
                t = t + 1
                continue
            # print(r, t)
            while r < len(mat) and t < len(mat[0]):
                if mat[r][t] == 0:
                    dist = dist + 1
                    t = t + 1
                    newrow.append(dist)
                else:
                    newrow.append(0)
                    break
            # x index
            t = t + 1
        # newrow.reverse()
        newmat.append(newrow)
        # row index
        r = r + 1
    new = np.matrix(newmat)
    return new, newmat


# vertical distance matrix
def vert_dist(mat):
    newmat = []
    # columns
    p = 0
    while p < len(mat[0]):
        new_column = []
        i = 0
        # values
        while i < len(mat):
            dist = 0
            if i == 0 or i == len(mat) - 1:
                new_column.append(0)
                i = i + 1
                continue
            while i < len(mat) and p < len(mat[0]):
                if mat[i][p] == 0:
                    dist = dist + 1
                    i = i + 1

                    new_column.append(dist)
                else:
                    new_column.append(0)
                    break
            # print(i, p)
            i = i + 1
        newmat.append(new_column)
        # print(len(newmat), len(newmat[0]))
        p = p + 1
    # newmat = list(zip(*newmat[::-1]))
    new = np.matrix(newmat)
    return new, newmat


# map box content: returns x1,x2,y1,y2 coordinates for bounding boxes
def map_content(mat):
    # Global variables
    boxes = []  # [[x1,x2,y1,y2], etc]

    # initialize rows
    for row in mat:
        row_index = mat.index(row)
        side_locations = []  # [[0,[]],...]
        down_queue = []  #
        t = 0
        while t < len(mat):
            side_locations.append([t, []])
            t = t + 1

        t = 0
        while t < len(mat[0]):
            down_queue.append([t, []])
            t = t + 1
        # Search for new Values  Values == Starting points to map a new thing
        for val in row:
            skip_val = False
            val_index = row.index(val)
            max_width = 0
            max_height = 0

            # Initial condidions
            # New starting value found
            if val != 0:
                for b in boxes:
                    if b[0] <= val_index <= b[1]:
                        if b[2] <= row_index <= b[3]:
                            skip_val = True
                            break
                if skip_val:
                    continue

                iterate_down = row_index
                while iterate_down != len(mat) - 1 and val_index != len(mat[0]):
                    # Search horizontally for
                    # Check if value exists within row
                    # Start searching left-right, and then down for each val in left/right
                    b = 0  # backward
                    while mat[iterate_down][val_index - b] != 0 and val_index - b != 0:
                        side_locations[iterate_down][1].append(val_index - b)
                        b = b + 1
                    back_width = b

                    f = 1  # forward
                    while (val_index + f) < len(mat[0]) and mat[iterate_down][val_index + f] != 0:
                        side_locations[iterate_down][1].append(val_index + f)
                        f = f + 1
                    forward_width = f
                    width = back_width + forward_width
                    if width > max_width:
                        max_width = width

                    # up
                    h = 0
                    for p in side_locations[iterate_down][1]:
                        d = 0
                        if p < len(mat[0]) and (iterate_down - d) not in down_queue[p][1]:
                            while (iterate_down - d) != 0 and mat[iterate_down - d][p] != 0:
                                down_queue[p][1].append(iterate_down + d)
                                d = d + 1
                            if d > h:
                                h = d
                    up = h

                    # down
                    h = 0
                    for p in side_locations[iterate_down][1]:
                        d = 0
                        if p < len(mat[0]) and (iterate_down + d) not in down_queue[p][1]:
                            while (iterate_down + d) < len(mat) and mat[iterate_down + d][p] != 0:
                                down_queue[p][1].append(iterate_down + d)
                                d = d + 1
                            if d > h:
                                h = d
                    down = h

                    height = up + down
                    if height > max_height:
                        max_height = height

                    iterate_down = iterate_down + 1

                # add box for each mapped data cluster
                x1 = val_index
                x2 = val_index + max_width
                y1 = row_index
                y2 = row_index + max_height
                cx = x1 + int(max_width / 2)
                cy = y1 + int(max_height / 2)

                if max_width < max_height:
                    radius = max_width
                else:
                    radius = max_height
                boxes.append([x1, x2, y1, y2, radius, cx, cy])
    return boxes
    # print("next iteration")
    # print("...row locations:", side_locations)
    # print("...Column locations:", down_queue)
    # print("...Len boxes:", len(boxes))
    # print("...Max Width height:", max_width, max_height)
