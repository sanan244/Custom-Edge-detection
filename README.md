# Custom-Edge-detection
This project serves as an educational example of detecting edges in images and how to customize this for effectiveness. Because of this many of the utility finctions are not optimized. If the user wishes to perform real-time video using openCV these functions will need to be optimized.

Main Driver File:

'rawimage.py'

Requirements:

A working desktop camera.'0' is the webcam default number for opencv(ex: cv2.VideoCapture(0))

Python 3

Modifications:

A portion of the code may be uncommented also able to draw bounding boxes over areas of the image based on RAW image edge data. No Machine Learning models are used to do this.
These edge related bounding boxes can be hypertuned to adjust user satisfaction.
