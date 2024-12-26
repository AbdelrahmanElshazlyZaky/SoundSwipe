import cv2
from ultralytics import YOLO
from shared_data.shared_data import SharedData

class ObjectDetection:


    def execute(self):
        # Load the trained model
        self.model = YOLO('E:\\new downloads\\fourth year\\HCI_Project\\python_server\\assets\\best.pt')
        print("Model loaded successfully.")
        
        self.previous_note=None
        while True:
            frame = SharedData.frame
            if frame is None:
                continue
        
            # Perform object detection
            results = self.model.predict(source=frame, conf=0.25, verbose=False)
            
            # Display detected classes
            for result in results:
                boxes = result.boxes
                if boxes is None:
                    self.previous_note=None
                if boxes is not None:
                    #print(f"Detected {len(boxes)} objects.")
                    for box in boxes:
                        cls = int(box.cls)  # Class ID
                        class_name = self.model.names[cls]  # Get class name from the model
                        conf = float(box.conf)  # Convert confidence score to float
                        print(f"Detected {class_name} with confidence {conf:.2f}")
                        if self.previous_note!=class_name or True:
                            SharedData.add_socket_data('object detection', class_name)
                            self.previous_note=class_name
            # # Annotate the frame
            # annotated_frame = results[0].plot()
            # cv2.imshow("YOLO Real-Time Detection", annotated_frame)
