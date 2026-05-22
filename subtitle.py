import cv2
import numpy as np
import time
#export DISPLAY=:0

def playVid(file):

    cv2.destroyAllWindows()

    if file < 10:
        file = '0' + str(file)
    else:
        file = str(file)
    file = 'subtitles/' + file + '.mp4'
    capture = cv2.VideoCapture(file)
    cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        isTrue, frame = capture.read()
        
        if cv2.waitKey(20) & 0xFF == ord('d') or not isTrue:
            break
        cv2.imshow("window", frame)
    cv2.destroyAllWindows()
    
def showBg():
    
    bg = np.zeros((1280, 480, 3), dtype=np.uint8)
    cv2.namedWindow("back", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("back", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    bg[1280: , 480: ] = (0, 0, 0)
    cv2.imshow("back", bg)

#showBg()
playVid(1)
#showBg()
time.sleep(2)
cv2.destroyAllWindows()