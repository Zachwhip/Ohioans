import serial
import threading
import time
import numpy as np
from datetime import datetime
import pandas as pd

stop_event = threading.Event()  # Event to signal the thread to stop

# Set your COM port and baud rate
com_port = 'COM3'  # Change this to your Arduino's COM port
baud_rate = 9600
time_array = []

# Open serial connection to Arduino
ser = serial.Serial(com_port, baud_rate, timeout=1)  # Added timeout for better reliability

def ir_beam_start():
    stop_event.clear()
    print("ir_beam_start")
    power_on = True
    time.sleep(2)
    while not stop_event.is_set():
        if ser.in_waiting > 0:
            # Read and decode serial data
            data = ser.readline().decode('utf-8').strip()
            
            if data:
                if power_on == True:
                    power_on = False
                    continue
                else:
                    # Print the received count data for debugging
                    print(f"Received: {data}")
                    
                    timestamp = datetime.now() #datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    time_array.append(timestamp)
                    print(f"Logged: {timestamp}")

def stop_monitoring():
    print("Stop event triggered for IR Beam.")
    time_array.clear()
    stop_event.set()  # Signal the background thread to stop