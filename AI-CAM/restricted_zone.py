from ultralytics import YOLO
import cv2
import os
from datetime import datetime

from database.database import create_database, save_event


# -----------------------------
# INITIALIZATION
# -----------------------------

create_database()

model = YOLO("yolo26n.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened")
    exit()


# -----------------------------
# CAMERA SETTINGS
# -----------------------------

CAMERA_ID = "CAM-01"
ZONE_NAME = "ZONE-A"


# -----------------------------
# RESTRICTED ZONE
# -----------------------------

ZONE_X1 = 200
ZONE_Y1 = 100
ZONE_X2 = 600
ZONE_Y2 = 400


# -----------------------------
# SNAPSHOT DIRECTORY
# -----------------------------

SNAPSHOT_DIR = "alerts/snapshots"

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


# Prevent saving the same event
# every single frame
active_alerts = set()


print("===================================")
print("       AI-CAM SECURITY SYSTEM")
print("===================================")
print("Camera :", CAMERA_ID)
print("Zone   :", ZONE_NAME)
print("Press Q to quit")
print()


# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break


    # Draw restricted zone

    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )


    # -----------------------------
    # YOLO TRACKING
    # -----------------------------

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=0.35,
        verbose=False
    )


    persons_inside = 0


    if results[0].boxes.id is not None:

        boxes = results[0].boxes.xyxy.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy()


        for box, cls, track_id in zip(
            boxes,
            classes,
            ids
        ):

            # Only persons

            if int(cls) != 0:
                continue


            x1, y1, x2, y2 = map(
                int,
                box
            )


            # Person center

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2


            # Check zone

            inside = (
                ZONE_X1 < center_x < ZONE_X2
                and
                ZONE_Y1 < center_y < ZONE_Y2
            )


            person_id = int(track_id)


            if inside:

                persons_inside += 1


                # Red bounding box

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    3
                )


                cv2.putText(
                    frame,
                    f"ALERT Person #{person_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )


                # -----------------------------
                # NEW ALERT
                # -----------------------------

                if person_id not in active_alerts:

                    active_alerts.add(person_id)


                    # Timestamp

                    now = datetime.now()

                    timestamp = now.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )


                    # Snapshot filename

                    filename = (
                        f"alert_"
                        f"{now.strftime('%Y%m%d_%H%M%S')}_"
                        f"person_{person_id}.jpg"
                    )


                    snapshot_path = os.path.join(
                        SNAPSHOT_DIR,
                        filename
                    )


                    # Save evidence

                    cv2.imwrite(
                        snapshot_path,
                        frame
                    )


                    # Save database event

                    save_event(
                        timestamp=timestamp,
                        camera_id=CAMERA_ID,
                        event_type="Restricted Zone Entry",
                        object_id=person_id,
                        zone=ZONE_NAME,
                        severity="HIGH",
                        snapshot=snapshot_path
                    )


                    print()
                    print("🚨 SECURITY ALERT")
                    print("Time      :", timestamp)
                    print("Camera    :", CAMERA_ID)
                    print("Person ID :", person_id)
                    print("Zone      :", ZONE_NAME)
                    print("Snapshot  :", snapshot_path)


            else:

                # Green box

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )


                cv2.putText(
                    frame,
                    f"Person #{person_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )


                # Person left zone

                if person_id in active_alerts:

                    active_alerts.remove(
                        person_id
                    )


    # -----------------------------
    # STATUS DISPLAY
    # -----------------------------

    if persons_inside > 0:

        cv2.putText(
            frame,
            "!!! SECURITY ALERT !!!",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.putText(
            frame,
            f"Persons in zone: {persons_inside}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    else:

        cv2.putText(
            frame,
            "SYSTEM STATUS: NORMAL",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    # Camera ID

    cv2.putText(
        frame,
        CAMERA_ID,
        (20, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # -----------------------------
    # DISPLAY
    # -----------------------------

    cv2.imshow(
        "AI-CAM Security Monitor",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()