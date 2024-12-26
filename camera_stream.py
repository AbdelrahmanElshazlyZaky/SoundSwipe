import threading
import time
import cv2

from shared_data.shared_data import SharedData


class CameraStream:
    def __init__(self):
        self.lock = SharedData.frame_lock
        self.running = True
        self.video_capture = cv2.VideoCapture(0)  # Initialize the camera

    def stream_video(self):
        while self.running:
            ret, frame = self.video_capture.read()
            if ret:
                with self.lock:
                    #self.frame = frame
                    SharedData.frame = frame
            time.sleep(0.01)  # Avoid overloading the CPU
            #To show Video
            #cv2.imshow('Video', frame)

    def stop_stream(self):
        self.running = False
        self.video_capture.release()
        cv2.destroyAllWindows()

    # def get_frame(self):
    #     with self.lock:
    #         return self.frame
