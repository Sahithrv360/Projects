from ultralytics import YOLO
import cv2

# Load pretrained YOLO model
model = YOLO("yolo26n.pt")

# Open laptop camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened")
    exit()

print("AI-CAM Tracking Started")
print("Press Q to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read frame")
        break

    # Object detection + tracking
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=0.35,
        verbose=False
    )
    if results[0].boxes.id is not None:

        ids = results[0].boxes.id.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()

        person_count = 0
        vehicle_count = 0

        for cls in classes:

            if int(cls) == 0:
                person_count += 1

            elif int(cls) in [2, 3, 5, 7]:
                vehicle_count += 1
        annotated_frame = results[0].plot()

        cv2.putText(
            annotated_frame,
            f"Persons: {person_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),    
            2
        )

        cv2.putText(
            annotated_frame,
            f"Vehicles: {vehicle_count}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
    # Draw tracking results

    # Display
    cv2.imshow(
        "AI-CAM - Object Tracking",
        annotated_frame
    )

    # Exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()