# Ohioans_File.py

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import Ohioans_Data

# A flag to control whether monitoring should continue
monitoring = True
stop_event = threading.Event()  # Event to signal the thread to stop
 
team_1_score = 0
team_2_score = 0

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        #move these somehwhere else. make sure theyre global variables
        #self.team_1_round_score = 0
        #self.team_2_round_score = 0
    def on_created(self, event):
        # This method is called when a new file is created
        if not event.is_directory:  # Only handle files (not directories)
            print(f"New file detected: {event.src_path}")
            # Add your file processing logic here
            Ohioans_Data.process_new_file(event.src_path)

def File_Find():
    global monitoring
    directory_to_watch = "C:/Users/dylan/Documents/ItemTest/TagLogs"
    
    print("Monitoring started...")

    # Set up the observer
    event_handler = NewFileHandler(directory_to_watch)
    observer = Observer()

    # Start observing the directory for file creation events
    observer.schedule(event_handler, directory_to_watch, recursive=False)

    # Start the observer in a separate thread
    observer.start()

    try:
        while not stop_event.is_set():  # Check if the stop event is set
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.stop()  # Stop the observer when the thread finishes
    observer.join()
    print("Monitoring stopped.")

def stop_monitoring():
    print("Stop event triggered.")
    stop_event.set()  # Signal the background thread to stop

def reset_stop_event():
    """Reset the stop_event flag to allow monitoring to start again."""
    stop_event.clear()
    print("Stop event cleared.")
