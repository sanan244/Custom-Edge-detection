# Two ways of implementing contours.
# Grey scale implementation: Find 'most common value' and
# compare pixels to that value. Draw a point wher the value changes

# Color images: Set current ration of rgb. If ration changes within
# threshold. Set rgb ratio to new value and draw point where it changed.

# both methods iterate pixels over rows

import time
from matplotlib import  pyplot as plt
from colorimg_utils import *
from greyscale_utils import *


def main():
    process_this_frame = True
    while True:
        if process_this_frame:
            cap = cv2.VideoCapture(0)
            time.sleep(1)
            ret, frame = cap.read()
            # cv2.imwrite(filename, frame)
            scale = 0.3
            rescale = int(1 / scale)
            dim = np.shape(frame.tolist())
            print("Dim:", dim)
            resized = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            threshold = .25  # how much noise is detected in the image
            box_padding = 10  # width and height of boxes to exclude bc of likely noise

            # visualize image dimensions and rgb values
            print("###############################################")
            print("Data for image with color...")
            """
            for f in frame:
                print("Length of array in global array:", len(f))
                for data in f:
                    print("Length of data in sub array:", len(data))
                    break
                break
                """
            # print("Length of Raw Data: ", len(frame))
            # print("Raw Data:\n", frame)

            # Process Raw Color image
            print("...Processing Color Image")
            ratio_matrix = matrix_ratio(resized)
            # print("Ratio Matrix:\n", ratio_matrix)

            # Edge detectors for left to right and up to down
            horzcontours, horzcontour_list = compare_horzratios(ratio_matrix, thresh=threshold)
            horzcontours, horzcontour_list = flip_matrix(horzcontour_list)
            # plt.matshow(horzcontours)
            # plt.show()

            vert_contours, vert_contour_list = compare_verti_ratios(ratio_matrix, thresh=threshold)
            # plt.matshow(vert_contours)
            # plt.show()

            # Add vertical and horizontal edge detectors
            contour = horzcontours + vert_contours
            contour_list = contour.tolist()
            # print("Combined edges:\n", contour)

            # Compute distances
            # horizontal
            horz1, horz1list = hor_dist(contour_list)
            flip_contour, flip_contourlist = flip_matrix(contour_list)
            horz2, horz2list = hor_dist(flip_contourlist)
            horz3, horz3list = flip_matrix(horz2list)
            horz = horz1 + horz3
            # plt.matshow(horz1, cmap="gray")
            # plt.matshow(horz2, cmap="gray")
            # plt.matshow(horz, cmap="gray")
            # plt.show()

            # Vertical
            vert1, vert1list = vert_dist(contour_list)
            vert1 = rotate_mat(vert1list)
            rotate_contourlist = rotate_mat(contour.tolist())
            rotate_contourlist = rotate_mat(rotate_contourlist)
            vert2, vert2list = vert_dist(rotate_contourlist)
            vert2list = rotate_mat(vert2list)
            vert2list = rotate_mat(vert2list)
            vert2list = rotate_mat(vert2list)
            vert2 = np.matrix(vert2list)
            vert2, vert2list = flip_matrix(vert2.tolist())
            vert = vert1 + vert2
            # plt.matshow(vert1, cmap="gray")
            # plt.matshow(vert2, cmap="gray")
            # plt.matshow(vert, cmap="gray")
            # plt.show()

            # Vertical + horizontal distance matrix
            boundary = horz + vert
            boundary, boundarylist = flip_matrix(boundary.tolist())
            #print("Combined distances:\n", boundary)
            # print(len(boundary.tolist()),len(boundary.tolist()[0]) )
            #plt.matshow(horzcontours)
            #plt.matshow(vert_contours)
            plt.matshow(boundary)
            plt.matshow(contour)
            plt.show()

            # Uncomment this large text block to create bounding boxes/bounding circles to the
            # edges using raw data and no ML
            """
            boxes = map_content(boundarylist)# this function can be hyper tuned to adjust the boxes on the raw data
            print("Boxes:", boxes)
            # plt.show()
            # return 0
            color = (255, 0, 0)
            for box in boxes:
                if (box[1] - box[0]) and (box[3] - box[2]) > box_padding:
                    radius = box[4] * rescale
                    cx = box[5] * rescale
                    cy = box[6] * rescale

                    x1 = box[0] * rescale
                    x2 = box[1] * rescale
                    y1 = box[2] * rescale
                    y2 = box[3] * rescale
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    #cv2.circle(frame, (cx, cy), radius, color)
            cv2.imshow("Original", frame)
            """

        process_this_frame = not process_this_frame
        # remove for video function to resume
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


main()
