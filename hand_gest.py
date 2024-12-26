import pickle
from dollarpy import Recognizer, Template, Point
import cv2
import mediapipe as mp
from shared_data.shared_data import SharedData
import numpy as np
class HandGesture:
    def __init__(self, templates_file="E:\\new downloads\\fourth year\\HCI_Project\\python_server\\assets\\final_templates.pkl"):
        self.templates = self.load_templates(templates_file)
        self.recognizer = Recognizer(self.templates)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_holistic = mp.solutions.holistic
    

    def load_templates(self, templates_file):
        try:
            with open(templates_file, "rb") as f:
                return pickle.load(f)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file {templates_file} not found.")
    
    def execute(self):
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            self.points = []
            self.left_shoulder, self.right_shoulder = [], []
            self.left_elbow, self.right_elbow = [], []
            self.left_wrist, self.right_wrist = [], []
            self.left_pinky, self.right_pinky = [], []
            self.left_index, self.right_index = [], []
            self.left_hip, self.right_hip = [], []

            process_this_frame = True

            while True:

                frame = SharedData.frame
                if frame is None:
                    continue

                if process_this_frame:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    results = holistic.process(image)
                    
                    # Convert the image back to BGR for display
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
                    # # Draw hand and pose landmarks
                    # self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
                    # self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
                    # self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                    #                         landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
                    try:
                        # Collect landmark points
                        self.left_shoulder.append(Point(results.pose_landmarks.landmark[11].x, results.pose_landmarks.landmark[11].y, 1))
                        self.right_shoulder.append(Point(results.pose_landmarks.landmark[12].x, results.pose_landmarks.landmark[12].y, 2))
                        self.left_elbow.append(Point(results.pose_landmarks.landmark[13].x, results.pose_landmarks.landmark[13].y, 3))
                        self.right_elbow.append(Point(results.pose_landmarks.landmark[14].x, results.pose_landmarks.landmark[14].y, 4))
                        self.left_wrist.append(Point(results.pose_landmarks.landmark[15].x, results.pose_landmarks.landmark[15].y, 5))
                        self.right_wrist.append(Point(results.pose_landmarks.landmark[16].x, results.pose_landmarks.landmark[16].y, 6))
                        self.left_pinky.append(Point(results.pose_landmarks.landmark[17].x, results.pose_landmarks.landmark[17].y, 7))
                        self.right_pinky.append(Point(results.pose_landmarks.landmark[18].x, results.pose_landmarks.landmark[18].y, 8))
                        self.left_index.append(Point(results.pose_landmarks.landmark[19].x, results.pose_landmarks.landmark[19].y, 9))
                        self.right_index.append(Point(results.pose_landmarks.landmark[20].x, results.pose_landmarks.landmark[20].y, 10))
                        self.left_hip.append(Point(results.pose_landmarks.landmark[23].x, results.pose_landmarks.landmark[23].y, 11))
                        self.right_hip.append(Point(results.pose_landmarks.landmark[24].x, results.pose_landmarks.landmark[24].y, 12))
                    except:
                        print("No valid landmarks detected in the current frame.")                    
                    
                    
                    self.points = (self.left_shoulder + self.right_shoulder + self.left_elbow + self.right_elbow +
                                    self.left_wrist +self.right_wrist +self.left_pinky + self.right_pinky +
                                    self.left_index +self.right_index +self.left_hip + self.right_hip)

                    try:
                        if len(self.points) > 1:
                            gesture = self.recognizer.recognize(self.points)
                            if gesture:
                                SharedData.add_socket_data('hand gesture', gesture)
                                #print(f"Recognized gesture: {gesture}")
                            else:
                                print("No gesture recognized.")
                        else:
                            print("Not enough points for recognition.")
                    except ZeroDivisionError:
                        print("Normalization failed due to zero scale. Skipping this frame.")
                process_this_frame = not process_this_frame