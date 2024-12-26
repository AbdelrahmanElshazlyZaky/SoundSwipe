import threading


class SharedData:
    _instance = None
    sokcetdata_lock = threading.Lock()
    serverdata_lock = threading.Lock()
    frame_lock = threading.Lock()

    #the data theat will be shared with the socket server
    _socket_data  = {}
    #the data that will be shared with the modules
    _server_data  = {}
    frame = None

    def add_socket_data(key, value):
        """Set the data to be shared with the socket server."""
        with SharedData.sokcetdata_lock: #critical section
            SharedData._socket_data[key] = value

    def get_socket_data_keys():
        """Get the data shared with the socket server."""
        return SharedData._socket_data.keys()
    def get_socket_data( key):
        """Get the data shared with the socket server."""
        data = None
        with SharedData.sokcetdata_lock:
            data = SharedData._socket_data.get(key, None)
        return data
    
    def add_server_data( key, value):
        """Set the data to be shared with the modules."""
        with SharedData.serverdata_lock:
            SharedData._server_data[key] = value
    def get_server_data_keys():
        return SharedData._server_data.keys()
    def get_server_data(key):
        """Get the data shared with the modules."""
        return SharedData._server_data.get(key, None)


    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            #cls._instance = super(Buffer, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the buffer data."""
        self.socket_data = []

    def add_item(self, item):
        """Add an item to the buffer."""
        self.socket_data.append(item)

    def get_all_items(self):
        """Retrieve all items in the buffer."""
        return self.socket_data

    def clear(self):
        """Clear the buffer."""
        self.socket_data = []

