from flask import *
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

app = Flask(__name__)

# Tracker variable indicating some changed happened or not: 1 -> Change while 0 -> No Change 
status = 1

class Watcher:

    DIRECTORY_TO_WATCH = "data/"

    # Initializing observer
    def __init__(self):
        self.observer = Observer()

    # Triggering listener thread 
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        # For this project we are monitoring only modification events. If modified status changes to 1
        elif event.event_type == 'modified':
            global status
            print("Received modified event - %s." % event.src_path)
            time.sleep(2)
            status = 1

# Sense API to track whether changes happened in the remote node/data_source or not
@app.route('/sense')
def sensor():
	return {'status': status}

# This endpoint will be used to obtain products data generally when the status changes to 1
@app.route('/read')
def reader():
	global status
	status = 0
	return send_file('data/products.csv', as_attachment=True)

# Class to handle the API service for the data_source
class App(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "API"
	def run(self):
		app.run(port=5001)

# Class to handle changes in the files in the given directory
class Change(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "Change"
	def run(self):
		w = Watcher()
		w.run()

if __name__ == '__main__':
	thread1 = App()
	thread2 = Change()
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()
	print("Exitting")