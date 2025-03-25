# Ohioans_Data.py
import Ohioans_Score
import Ohioans_IR as IR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.stats import kurtosis
from datetime import datetime, timedelta

team_1_tid = '1111BBBB'
team_2_tid = '2222BBBB'

def lowpass_filter(data, cutoff=0.1, fs=1.0, order=5): #fs maybe 1000
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

def process_new_file(file_path):
    """Process the new file."""
    print(f"Processing file: {file_path}")
    
    # Try to read the CSV file with error handling for bad lines
    try:
        # Resets hole and board count variables
        team_1_hole_count = 0
        team_1_board_count = 0
        team_2_hole_count = 0
        team_2_board_count = 0

        # Set column names
        column_names = [
            'Timestamp', 'EPC', 'TID', 'Antenna', 'RSSI', 'Frequency',
            'Hostname', 'PhaseAngle', 'DopplerFrequency'
        ]
        
        # Read the CSV with custom column names and skip the metadata
        df = pd.read_csv(file_path, skiprows=3, index_col=False, names=column_names)

        # Clean dataframe
        #df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
        df["RSSI"] = pd.to_numeric(df["RSSI"], errors='coerce')
        df = df.dropna(subset=["Timestamp", "EPC", "RSSI"])

        # Get first and last RFID read
        first_read_string = df["Timestamp"].iloc[0]
        first_read_time = datetime.fromisoformat(first_read_string)
        first_read_time = first_read_time.replace(tzinfo=None) # Remove timezone
        last_read_string = df["Timestamp"].iloc[-1]
        last_read_time = datetime.fromisoformat(last_read_string)
        last_read_time = last_read_time.replace(tzinfo=None)

        # Get all bags read by RFID reader
        unique_epcs = df["EPC"].unique()

        # Do stuff with each bag
        for epc in unique_epcs:
            # New dataframe with only data from active EPC
            epc_data = df[df["EPC"] == epc]

            # Skip bag if it has less than 20 reads (code will break if a bag has less than 19 reads for some reason)
            if len(epc_data) < 20: 
                continue

            # Adds 1 board point since bag was detected
            if team_1_tid in epc:
                team_1_board_count += 1
            elif team_2_tid in epc:
                team_2_board_count += 1
            
            # Find window where bag is first detected
            mid_bound_string = epc_data["Timestamp"].iloc[0] # First timestamp
            mid_bound_tz = datetime.fromisoformat(mid_bound_string) # Convert string to datetime
            mid_bound = mid_bound_tz.replace(tzinfo=None) # Remove timezone
            mid_bound = mid_bound + timedelta(seconds=3) # Offset time to better align with IR beam timestamp

            # Fnd left and right bounds (-2 and +2 seconds from first read)
            left_bound = mid_bound - timedelta(seconds=2)
            right_bound = mid_bound + timedelta(seconds=2)

            # Search if there is an IR trigger when bag is first detected
            # This will detect if a bag was thrown directly in the hole
            trigger_len = len(IR.time_array)
            for i in range(trigger_len):
                trigger_time = IR.time_array[i]
                if trigger_time >= left_bound and trigger_time <= right_bound:
                    print(epc, "went in the HOLE at", trigger_time)
                    if team_1_tid in epc:
                        team_1_hole_count += 1
                        break
                    else:
                        team_2_hole_count += 1
                        break
                else:
                    print(epc, "did not go in the hole at", trigger_time)

            # epc_data_np = epc_data['RSSI'].to_numpy() #convert dataframe RSSI values into numpy values
            # filtered_rssi = lowpass_filter(epc_data_np) #apply lowpass filter to RSSI values
            # gradient_rssi = np.gradient(filtered_rssi) #calculate gradient
            # gradient_kurtosis = kurtosis(gradient_rssi, fisher=True) #calculate kurtosis
            # print("kurtosis of", epc, "is", gradient_kurtosis)
            # epc_data = epc_data.iloc[:] #trim start:end

        # Reset and calculate round score
        team_1_round_score = 0
        team_2_round_score = 0

        # Calculate score
        team_1_round_score = (team_1_board_count - team_1_hole_count) + (team_1_hole_count * 3)
        team_2_round_score = (team_2_board_count - team_2_hole_count) + (team_2_hole_count * 3)
        if team_1_round_score > team_2_round_score:
            team_1_round_score = team_1_round_score - team_2_round_score
            team_2_round_score = 0
        elif team_2_round_score > team_1_round_score:
            team_2_round_score = team_2_round_score - team_1_round_score
            team_1_round_score = 0
        else:
            team_1_round_score = 0
            team_2_round_score = 0

        # Update scores on UI
        game_scores = Ohioans_Score.GameScores()
        game_scores.update_scores(team_1_round_score, team_2_round_score)
        IR.time_array.clear()
        
    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


    

