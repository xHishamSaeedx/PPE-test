from ultralytics import YOLO
import cv2
import cvzone
import math

#cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
cap = cv2.VideoCapture("../Videos/ppe-2.mp4")


model = YOLO("best.pt")

classNames = [
    "Hardhat",
    "Mask",
    "NO-Hardhat",
    "NO-Mask",
    "NO-Safety Vest",
    "Person",
    "Safety Cone",
    "Safety Vest",
    "machinery",
    "vehicle"
]
myColor = (0,0,255)
while True:
    success, img = cap.read()
    results = model(img, stream = True)
    for r in results:
        boxes = r.boxes
        for box in boxes:

            #bounding box
            x1,y1,x2,y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
            #cv2.rectangle(img, (x1, y1) , (x2,y2) ,(255,0, 255), 3 )
            w,h = x2-x1, y2-y1

            #cvzone.cornerRect(img, (x1,y1,w,h))
            cv2.rectangle(img, (x1,y1) , (x2,y2) , myColor , 3)

            conf = math.ceil((box.conf[0]*100))/100

            cls = box.cls[0]
            currentClass = classNames[int(cls)]
            if currentClass in ["Hardhat","Mask","Safety Cone","Safety Vest"] :
                myColor = (0,255,0)
            elif currentClass in ["Person","machinery","vehicle"]:
                myColor = (255, 0, 0)
            else:
                myColor = (0,0,255)

            cvzone.putTextRect(img, f"{classNames[int(cls)]} {conf}" , (max(0,x1),max(35,y1)), scale = 0.75, thickness= 1, colorB=myColor, colorT=(255,255,255), colorR=myColor)



    cv2.imshow("image", img)
    cv2.waitKey(1)