import cv2
import numpy as np
import mediapipe as mp
import threading
from shared_data.shared_data import SharedData
import json
class GazeTracking:
    def __init__(self, scale_factor=10,json_file="gaze_data.json"):
        self.scale_factor = scale_factor
        self.heatmap = None
        self.stop_event = threading.Event()
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.gaze_data = []  # List to store gaze points
        self.json_file = json_file

    def initialize_heatmap(self,frame_shape):
         self.heatmap = np.zeros((frame_shape[0], frame_shape[1]), dtype=np.float32)

    def improved_gaze(self, frame, points):
        """Processes a frame to detect and compute gaze direction without drawing lines or circles."""
        left_eye_points = [33, 133, 160, 159, 158, 144, 153, 145]
        right_eye_points = [362, 263, 387, 386, 385, 373, 380, 374]

        left_eye_center = np.mean([
            (int(points.landmark[i].x * frame.shape[1]), int(points.landmark[i].y * frame.shape[0]))
            for i in left_eye_points
        ], axis=0).astype(int)

        right_eye_center = np.mean([
            (int(points.landmark[i].x * frame.shape[1]), int(points.landmark[i].y * frame.shape[0]))
            for i in right_eye_points
        ], axis=0).astype(int)

        left_pupil = (
            int(points.landmark[468].x * frame.shape[1]),
            int(points.landmark[468].y * frame.shape[0])
        )
        right_pupil = (
            int(points.landmark[473].x * frame.shape[1]),
            int(points.landmark[473].y * frame.shape[0])
        )

        left_gaze_vector = (left_pupil[0] - left_eye_center[0], left_pupil[1] - left_eye_center[1])
        right_gaze_vector = (right_pupil[0] - right_eye_center[0], right_pupil[1] - right_eye_center[1])

        left_gaze_end = (
            left_pupil[0] + left_gaze_vector[0] * self.scale_factor,
            left_pupil[1] + left_gaze_vector[1] * self.scale_factor
        )
        right_gaze_end = (
            right_pupil[0] + right_gaze_vector[0] * self.scale_factor,
            right_pupil[1] + right_gaze_vector[1] * self.scale_factor
        )

    # Removed cv2.arrowedLine and cv2.circle calls to avoid drawing on the frame.

        return left_gaze_end, left_gaze_vector

    def save_gaze_point(self, point):
        """Save a single gaze point to the gaze data list."""
        self.gaze_data.append({"x": int(point[0]), "y": int(point[1])})

    def save_gaze_data_to_json(self):
        """Save all collected gaze points to a JSON file."""
        with open(self.json_file, "w") as file:
            json.dump(self.gaze_data, file, indent=4)

    def draw_heatmap_from_json(self):
        """Draw a heatmap using gaze points saved in the JSON file."""
        with open(self.json_file, "r") as file:
            gaze_data = json.load(file)

        for point in gaze_data:
            x, y = point["x"], point["y"]
            if 0 <= x < self.heatmap.shape[1] and 0 <= y < self.heatmap.shape[0]:
                cv2.circle(self.heatmap, (x, y), 2, 1, -1)

        self.save_heatmap("final_heatmap_from_json.png")

    def apply_heatmap(self, frame):
        """Overlay heatmap on the frame."""
        normalized = cv2.normalize(self.heatmap, None, 0, 255, cv2.NORM_MINMAX)
        colored = cv2.applyColorMap(normalized.astype(np.uint8), cv2.COLORMAP_JET)
        return cv2.addWeighted(frame, 0.6, colored, 0.4, 0)

    def save_heatmap(self, filename="heatmap.png"):
        """Save the heatmap as an image file."""
        normalized = cv2.normalize(self.heatmap, None, 0, 255, cv2.NORM_MINMAX)
        colored = cv2.applyColorMap(normalized.astype(np.uint8), cv2.COLORMAP_JET)
        cv2.imwrite(filename, colored)

    def execute(self):
        """Main execution method for processing the video stream."""
        process_this_frame = True

        while True:
                frame = SharedData.frame  # Assuming frame is fetched from a shared data source
                if frame is None:
                    continue

                if self.heatmap is None:
                    self.initialize_heatmap(frame.shape[:2])

                if process_this_frame:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.mp_face_mesh.process(image)

                    if results.multi_face_landmarks:
                        points = results.multi_face_landmarks[0]
                        left_gaze_end, left_gaze_vector = self.improved_gaze(frame, points)
                        self.save_gaze_point(left_gaze_end)

                    output_frame = self.apply_heatmap(frame)
                    SharedData.add_socket_data("gaze_heatmap", output_frame)
                    self.save_gaze_data_to_json()
                    self.draw_heatmap_from_json()

                process_this_frame = not process_this_frame  # Skip alternate frames
 
           

    def stop(self):
        """Stop the processing thread."""
        self.stop_event.set()
