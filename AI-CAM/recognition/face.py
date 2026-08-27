from insightface.app import FaceAnalysis
import cv2
import os
import numpy as np


class FaceRecognizer:

    def __init__(self):

        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

        self.known_faces = {}


    def load_face(self, image_path, name):

        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not read {image_path}")
            return

        faces = self.app.get(image)

        if len(faces) == 0:
            print(f"No face found in {image_path}")
            return

        embedding = faces[0].embedding

        embedding = embedding / np.linalg.norm(
            embedding
        )

        self.known_faces[name] = embedding

        print(f"Registered: {name}")


    def load_database(self, folder="faces"):

        if not os.path.exists(folder):
            return

        for filename in os.listdir(folder):

            if filename.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                path = os.path.join(
                    folder,
                    filename
                )

                name = os.path.splitext(
                    filename
                )[0]

                self.load_face(
                    path,
                    name
                )


    def recognize(self, face_embedding):

        if len(self.known_faces) == 0:
            return "Unknown", 0.0

        embedding = face_embedding / np.linalg.norm(
            face_embedding
        )

        best_name = "Unknown"
        best_score = 0.0

        for name, known_embedding in self.known_faces.items():

            score = np.dot(
                embedding,
                known_embedding
            )

            if score > best_score:

                best_score = score
                best_name = name

        # Recognition threshold
        if best_score < 0.45:
            return "Unknown", best_score

        return best_name, best_score