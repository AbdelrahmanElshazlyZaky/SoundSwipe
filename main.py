from connection.connection_service import SocketServer
from features.face_recg import FaceRecognition
from features.obj_detect import ObjectDetection
from features.emotion_detect import EmotionDetection
from features.bluet import DiscoverDevice
from stream.camera_stream import CameraStream
from threads_manager.thread_manager import ThreadManager
from features.gaze import GazeTracking
from features.hand_gest import HandGesture

if __name__ == "__main__":
    
    #init the services
    thread_manager = ThreadManager()
    cam_stream = CameraStream()
    server = SocketServer(ip_address='127.0.0.1', port_number=5000)

    face_rec=FaceRecognition()
    obj_detection=ObjectDetection()
    emotion_det=EmotionDetection()
    bluetooth=DiscoverDevice()
    gaze=GazeTracking()
    hand_gest=HandGesture()
    #add the threads to the thread manager
    thread_manager.add_thread(server.start_server)
    thread_manager.add_thread(cam_stream.stream_video)

    thread_manager.add_thread(face_rec.execute)
    thread_manager.add_thread(obj_detection.execute)
    thread_manager.add_thread(emotion_det.execute)
    thread_manager.add_thread(bluetooth.execute)
    thread_manager.add_thread(gaze.execute)
    thread_manager.add_thread(hand_gest.execute)


    #start the threads
    thread_manager.start_threads()
    thread_manager.join_threads()  