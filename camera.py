import cv2
import parseFrame as fparse
import numpy as np

def scanPuzzle():
    f = 0
    found = False
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval and not found and f < 1800:
        f+=1

        cv2.rectangle(frame, (480, 120), (1440, 940), (0,255,0), 3)
        cv2.imshow("preview",frame)
        
        rval, frame = vc.read()

        found, puzzle = fparse.findPhone(frame)

        key = cv2.waitKey(20)
        if key == 27:
            break

    vc.release()
    cv2.destroyWindow("preview")
    return puzzle
    