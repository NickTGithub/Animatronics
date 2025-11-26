import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview

cam = Picamera2()
cam.configure(cam.create_preview_configuration(lores={"size": (120, 90)}, display="lores")
)
cam.start()

np.random.seed(20)
class Detector:
    def __init__(self,videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')

        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList), 3))

        #print(self.classesList)

    def onVideo(self):

        image = cam.capture_array()
        image = image[:, :, :3] 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        while True:
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold = 0.5)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0])
            confidences = list(map(float,confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.5, nms_threshold=0.2)

            if len(bboxIdx) !=0:
                for i in range(0,len(bboxIdx)):

                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]
                    classColor = [int(c) for c in self.colorList[classLabelID]]

                    displayText = "{}:{:.2f}".format(classLabel,classConfidence)

                    x,y,w,h = bbox

                    cv2.rectangle(image, (x,y), (x+w, y+h), color = classColor, thickness=1)
                    cv2.putText(image, displayText, (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor,2)

            cv2.imshow("result", image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

            image = cam.capture_array() 
            image = image[:, :, :3]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.destroyAllWindows()

videoPath = 2
modelPath = 'model_data/frozen_inference_graph.pb'
configPath = 'model_data/ssd_mobilenet_v3_large_coco.pbtxt'
classesPath = 'model_data/coco.names'

def main():
    videoPath = 2

    configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("model_data", "coco.names")

    detector = Detector(videoPath, configPath, modelPath, classesPath)
    detector.onVideo()

if __name__ == '__main__':
    main()