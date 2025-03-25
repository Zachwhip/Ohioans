# Ohioans1.0.py

###################################################
# Ohioans cornhole itemtest log file reader
# Build using the following command
# pyinstaller Ohioans1.0.py --noconfirm --noconsole
###################################################

import threading
import Ohioans_UI
import Ohioans_File
import Ohioans_IR

def start_program():
    print("Program started")
    
    # Reset the stop event before starting the monitoring thread again
    Ohioans_File.reset_stop_event()
    
    # Start the file monitoring in a separate thread to keep the UI responsive
    file_monitor_thread = threading.Thread(target=Ohioans_File.File_Find)
    file_monitor_thread.daemon = True
    file_monitor_thread.start()

    # Start IR beam monitor
    ir_monitor_thread = threading.Thread(target=Ohioans_IR.ir_beam_start)
    ir_monitor_thread.daemon = True
    ir_monitor_thread.start()

def stop_program():
    print("Program stopped")
    # Signal the monitoring thread to stop
    Ohioans_File.stop_monitoring()
    Ohioans_IR.stop_monitoring()
    Ohioans_File.team_1_score = 0
    Ohioans_File.team_2_score = 0

if __name__ == "__main__":
    Ohioans_UI.run(start_program, stop_program)