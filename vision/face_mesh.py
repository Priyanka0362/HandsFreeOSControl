import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import RunningMode


class FaceMeshDetector:

    def __init__(self):

        options = vision.FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="assets/face_landmarker.task"
            ),
            running_mode=RunningMode.IMAGE,
            num_faces=1,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.detector.detect(mp_image)

        return result