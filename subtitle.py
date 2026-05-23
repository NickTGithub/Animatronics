import cv2
import numpy as np
import time
#export DISPLAY=:0

cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
bg = cv2.imread('background.jpg')

def playVid(file):

    if file < 10:
        file = '0' + str(file)
    else:
        file = str(file)
    file = 'subtitles/' + file + '.mp4'
    print('playing ' + file)
    capture = cv2.VideoCapture(file)



    while True:
        isTrue, frame = capture.read()
        
        if cv2.waitKey(20) & 0xFF == ord('d') or not isTrue:
            break
        cv2.imshow("window", frame)



def showBg():
    global bg
    cv2.waitKey(20)
    cv2.imshow("window", bg)
    cv2.waitKey(20)

# for i in range(1,32):
#     playVid(i)
# playVid(17)
showBg()
# time.sleep(3)
# cv2.destroyAllWindows()