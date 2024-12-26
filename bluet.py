
import numpy as np
import json
import os
import threading
from shared_data.shared_data import SharedData
import bluetooth



class DiscoverDevice:
    def __init__(self):
        # Initialize a threading event to control the thread's lifecycle
        self.stop_event = threading.Event()
        pass
    
    JSON_FILE = "E:\\new downloads\\fourth year\\HCI_Project\\python_server\\assets\\bluetooth_devices.json"

    def load_known_devices(self,file_path):
        """
        Load known devices from a JSON file.
        """
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file).get("users", [])
        return []
    
    def discover_bluetooth_devices(self):
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        devices_list = [{"address": addr, "name": name} for addr, name in nearby_devices]
        return devices_list
    
    
    
    def execute(self):
    # Load known persons from the JSON file
        known_devices = self.load_known_devices(self.JSON_FILE)

        while True:


                devices_data = self.discover_bluetooth_devices()
                known_addresses = [device['address'] for device in known_devices]

                matches = [device for device in devices_data if device['address'] in known_addresses]
                #print(f"Matches: {matches}")
                #print(f"Known addresses: {known_addresses}")
                # If a match was found in known_face_encodings, just use the first one.
                if matches:
                    
                    matched_device = matches[0]  # Take the first matched device
                    name = matched_device.get('name', 'Unknown')
                    address = matched_device.get('address')
                    print(f"First known device found: {name} ({address})")

                    SharedData.add_socket_data('bluetooth', name)
                    # self.stop_event.set()
                    return
              
