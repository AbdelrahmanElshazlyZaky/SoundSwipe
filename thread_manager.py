import cv2
import threading


class ThreadManager:
    def __init__(self):
        self.threads = []

    def add_thread(self, thread_function, *args):
        thread = threading.Thread(target=thread_function, args= args)
        self.threads.append(thread)
        return thread

    def start_threads(self):
        for thread in self.threads:
            thread.start()


    def join_threads(self):
        for thread in self.threads:
            thread.join()

