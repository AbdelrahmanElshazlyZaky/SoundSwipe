import socket
from time import sleep
from shared_data.shared_data import SharedData


class SocketServer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Corrected this line
        return cls._instance

    def __init__(self, ip_address='localhost', port_number=5000):
        if not hasattr(self, 'server_socket'):  # Prevent reinitialization
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((ip_address, port_number))
            self.server_socket.listen(5)
            self.running = True
            print(f"Socket server started at {ip_address}:{port_number}. Waiting for connections...")

    def start_server(self):
        try:
            while self.running:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection established with {addr}")
                self.handle_client(client_socket)
                client_socket.close()
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            self.stop_server()

    def handle_client(self, client_socket):
        """Send data from SharedData to the connected client."""
        while self.running:
            for key in list(SharedData.get_socket_data_keys()):
                if SharedData.get_socket_data(key) is not None:
                    self.send_data(client_socket,str(key)+":"+str(SharedData.get_socket_data(key)))
                    SharedData.add_socket_data(key,None) 
                    print(f"Data sent for key {key}.")
                sleep(1)

    def send_data(self, client_socket, data):
        """Send data to the client."""
        try:
            client_socket.sendall(data.encode('utf-8'))
        except BrokenPipeError:
            print("Connection broken while sending data.")

    def stop_server(self):
        """Stop the server and release resources."""
        self.running = False
        self.server_socket.close()
        print("Socket server stopped.")

    def __del__(self):
        self.stop_server()

