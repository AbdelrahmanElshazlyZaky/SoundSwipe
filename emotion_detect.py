import cv2
from deepface import DeepFace
import json
from shared_data.shared_data import SharedData

class EmotionDetection:
    def __init__(self):
        pass
        
    # Specify the emotions to analyze
    

    def execute(self):
        # # Load the pre-trained DeepFace model
        # DeepFace.build_model('Emotion')
        # print("Model loaded successfully.")
        self.required_outputs = ['emotion']
        while True:
            frame = SharedData.frame
            if frame is None:
                continue
                    
            # Convert the BGR frame to RGB (DeepFace expects RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                # Analyze the frame for facial expressions (emotion)
                result = DeepFace.analyze(rgb_frame, actions=self.required_outputs, enforce_detection=False)
                # Display the results for each detected face
                for face_result in result:
                    # Get the detected emotion with the highest confidence
                    emotion = face_result['dominant_emotion']
                    confidence = face_result['emotion'][emotion]
                    with open('E:\\new downloads\\fourth year\\HCI_Project\\python_server\\assets\\analysis_results.json', 'w') as json_file:
                        json.dump(result, json_file, indent=4, sort_keys=True)
                    
                    # Print the JSON content to the console
                    # print("\nFull JSON Output:")
                    # print(json.dumps(result, indent=4, sort_keys=True))
                    # Ensure the region is unpacked properly (x, y, w, h)
                    # region = face_result['region']
                    # x, y, w, h = region['x'], region['y'], region['w'], region['h']
                    SharedData.add_socket_data('emotion detection', emotion)
                    # # Draw bounding box around the face (Optional)
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # # Display the emotion and confidence on the frame
                    # cv2.putText(frame, f"{emotion}: {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            except Exception as e:
                print(f"Face analysis error: {e}")
            
    