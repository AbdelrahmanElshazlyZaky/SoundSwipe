import bluetooth
import json
import socket

def discover_bluetooth_devices():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    devices_list = {
        "users": [{"address": addr, "name": name} for addr, name in nearby_devices]
    }
    return devices_list

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))  # Replace with the desired port
    server_socket.listen(5)
    print("Socket server started. Waiting for connection...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Discover and send Bluetooth data as JSON
        devices_data = discover_bluetooth_devices()
        data_json = json.dumps(devices_data)
        client_socket.sendall(data_json.encode('utf-8'))

        client_socket.close()

if __name__ == "__main__":
    start_server()
