import cv2
import face_recognition
import numpy as np
import json
import os
import threading
from shared_data.shared_data import SharedData

class FaceRecognition:
    def __init__(self):
        # Initialize a threading event to control the thread's lifecycle
        self.stop_event = threading.Event()
    # Path to the JSON file
    JSON_FILE = "E:\\new downloads\\fourth year\\HCI_Project\\python_server\\assets\\known_persons.json"

    # Function to load the known persons from the JSON file
    def load_known_persons(self):
        if os.path.exists(self.JSON_FILE):
            with open(self.JSON_FILE, "r") as file:
                return json.load(file)
        return {}

    # Function to save the known persons to the JSON file
    def save_known_persons(self,data):
        with open(self.JSON_FILE, "w") as file:
            json.dump(data, file, indent=4)

    # Function to add a new person to the JSON file
    def add_known_person(self,name, face_encoding):
        known_persons = self.load_known_persons()
        
        # If the person is already in the database, do nothing
        if name in known_persons:
            print(f"{name} is already in the database.")
        else:
            # Convert numpy array to a list before saving
            known_persons[name] = {"face_encoding": face_encoding.tolist()}
            self.save_known_persons(known_persons)
            print(f"{name} has been added to the database.")
        
        # Return the updated known persons dictionary
        return known_persons
    def execute(self):
    # Load known persons from the JSON file
        known_persons = self.load_known_persons()

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True


        # This variable ensures that we only ask for a name once
        name_entered = False
        debug=True
        while True:
            # Grab a single frame of video
            frame = SharedData.frame
            #dont process if frame is None

            if frame is None:
                continue

            # Only process every other frame of video to save time
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
                
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # Check for matches with known faces
                    matches = face_recognition.compare_faces([person['face_encoding'] for person in known_persons.values()], face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        
                        first_match_index = matches.index(True)
                        name = list(known_persons.keys())[first_match_index]
                        SharedData.add_socket_data('face recognition', name)
                        self.stop_event.set()
                        return
                    # If no match was found, ask the user for the person's name and add them to the database
                    if name == "Unknown" and not name_entered:
                        SharedData.add_socket_data('face recognition', "New person detected, please enter his name:")
                        #print("New person detected, please enter their name:")
                        # name = input()
                        known_persons = self.add_known_person(name, face_encoding)  # Add new person to the database
                        # name_entered = True  # Set to True so it doesn't ask again for this person

                    #face_names.append(name)


            process_this_frame = not process_this_frame
