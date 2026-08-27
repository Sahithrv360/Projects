from ultralytics import YOLO
import cv2

model = YOLO("yolo26n.pt")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error Camera could not be found")
    exit()

print("AI-CAM started")
print("Press Q to quit")

while True:
    ret,frame = cap.read()

    if not ret:
        print('ERROR: could not read frame')
        break

    results = model(frame,conf=0.5,verbose=False)

    annotated_frame = results[0].plot()

    cv2.imshow("AI-CAM",annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("AI-CAM stopped")