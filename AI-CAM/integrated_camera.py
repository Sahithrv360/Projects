from ultralytics import YOLO
from insightface.app import FaceAnalysis

import cv2
import numpy as np
import os

from datetime import datetime

from database.database import create_database, save_event


# ==========================================
# INITIALIZATION
# ==========================================

create_database()

# YOLO
yolo = YOLO("yolo26n.pt")


# Face model
face_app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

face_app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


# ==========================================
# REGISTERED PEOPLE
# ==========================================

known_faces = {}


def load_faces():

    folder = "faces"

    if not os.path.exists(folder):
        return

    for filename in os.listdir(folder):

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        path = os.path.join(
            folder,
            filename
        )

        image = cv2.imread(path)

        if image is None:
            continue

        faces = face_app.get(image)

        if len(faces) == 0:
            print(
                f"No face found: {filename}"
            )
            continue

        embedding = faces[0].embedding

        embedding = embedding / np.linalg.norm(
            embedding
        )

        name = os.path.splitext(
            filename
        )[0]

        known_faces[name] = embedding

        print(
            f"Registered person: {name}"
        )


load_faces()


# ==========================================
# FACE RECOGNITION
# ==========================================

def recognize_face(embedding):

    if len(known_faces) == 0:
        return "Unknown", 0.0

    embedding = embedding / np.linalg.norm(
        embedding
    )

    best_name = "Unknown"
    best_score = 0.0

    for name, known_embedding in known_faces.items():

        score = np.dot(
            embedding,
            known_embedding
        )

        if score > best_score:

            best_score = score
            best_name = name

    if best_score < 0.45:

        return "Unknown", best_score

    return best_name, best_score


# ==========================================
# CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERROR: Camera unavailable")
    exit()


# ==========================================
# RESTRICTED ZONE
# ==========================================

ZONE_X1 = 200
ZONE_Y1 = 100

ZONE_X2 = 600
ZONE_Y2 = 400


# ==========================================
# ALERT STORAGE
# ==========================================

os.makedirs(
    "alerts/snapshots",
    exist_ok=True
)

active_alerts = set()


print()
print("====================================")
print("       AI-CAM INTEGRATED SYSTEM")
print("====================================")
print("YOLO       : ONLINE")
print("Face AI    : ONLINE")
print("Tracking   : ONLINE")
print("Camera     : ONLINE")
print()
print("Press Q to quit")
print()


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        break


    # --------------------------------------
    # Draw restricted zone
    # --------------------------------------

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


    # --------------------------------------
    # YOLO detection + tracking
    # --------------------------------------

    results = yolo.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=0.35,
        verbose=False
    )


    if results[0].boxes.id is None:

        cv2.imshow(
            "AI-CAM",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        continue


    boxes = results[0].boxes.xyxy.cpu().numpy()

    classes = results[0].boxes.cls.cpu().numpy()

    ids = results[0].boxes.id.cpu().numpy()


    # ======================================
    # PROCESS PERSONS
    # ======================================

    for box, cls, track_id in zip(
        boxes,
        classes,
        ids
    ):

        # Class 0 = person

        if int(cls) != 0:
            continue


        x1, y1, x2, y2 = map(
            int,
            box
        )

        person_id = int(track_id)


        # ----------------------------------
        # Person center
        # ----------------------------------

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2


        # ----------------------------------
        # Restricted zone check
        # ----------------------------------

        inside_zone = (
            ZONE_X1 < center_x < ZONE_X2
            and
            ZONE_Y1 < center_y < ZONE_Y2
        )


        # ----------------------------------
        # Crop person's region
        # ----------------------------------

        person_crop = frame[
            max(0, y1):min(frame.shape[0], y2),
            max(0, x1):min(frame.shape[1], x2)
        ]


        person_name = "Unknown"
        face_score = 0.0


        # ----------------------------------
        # Face recognition
        # ----------------------------------

        if person_crop.size > 0:

            faces = face_app.get(
                person_crop
            )

            if len(faces) > 0:

                face = faces[0]

                person_name, face_score = recognize_face(
                    face.embedding
                )


        # ==================================
        # DISPLAY
        # ==================================

        if person_name == "Unknown":

            box_color = (0, 165, 255)

        else:

            box_color = (0, 255, 0)


        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            box_color,
            2
        )


        label = (
            f"{person_name} "
            f"ID:{person_id} "
            f"{face_score:.2f}"
        )


        cv2.putText(
            frame,
            label,
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            box_color,
            2
        )


        # ==================================
        # RESTRICTED ZONE ALERT
        # ==================================

        if inside_zone:

            if person_id not in active_alerts:

                active_alerts.add(
                    person_id
                )


                now = datetime.now()

                timestamp = now.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )


                filename = (
                    f"alert_"
                    f"{now.strftime('%Y%m%d_%H%M%S')}_"
                    f"person_{person_id}.jpg"
                )


                snapshot = os.path.join(
                    "alerts/snapshots",
                    filename
                )


                cv2.imwrite(
                    snapshot,
                    frame
                )


                # ----------------------------------
                # Determine event
                # ----------------------------------

                if person_name == "Unknown":

                    event_type = (
                        "Unknown Person "
                        "in Restricted Zone"
                    )

                    severity = "CRITICAL"

                else:

                    event_type = (
                        "Registered Person "
                        "in Restricted Zone"
                    )

                    severity = "HIGH"


                # ----------------------------------
                # Database
                # ----------------------------------

                save_event(
                    timestamp,
                    "CAM-01",
                    event_type,
                    person_id,
                    "ZONE-A",
                    severity,
                    snapshot
                )


                print()
                print("🚨 SECURITY EVENT")
                print("--------------------------")
                print("Person :", person_name)
                print("ID     :", person_id)
                print("Zone   : ZONE-A")
                print("Time   :", timestamp)
                print("Level  :", severity)
                print("Image  :", snapshot)


        else:

            if person_id in active_alerts:

                active_alerts.remove(
                    person_id
                )


    # ======================================
    # SYSTEM STATUS
    # ======================================

    cv2.putText(
        frame,
        "AI-CAM ONLINE",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        "YOLO + FACE AI + TRACKING",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # ======================================
    # DISPLAY
    # ======================================

    cv2.imshow(
        "AI-CAM Security System",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()