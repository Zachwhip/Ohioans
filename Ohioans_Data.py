# Ohioans_Data.py

import pandas as pd
import sys
import Ohioans_File
import Ohioans_Score

def process_new_file(file_path):
    """Process the new file."""
    print(f"Processing file: {file_path}")
    
    # Try to read the CSV file with error handling for bad lines
    try:
        # Skip the first 3 lines (metadata lines) and read the file
        # Manually define the correct column names
        column_names = [
            'Timestamp', 'EPC', 'TID', 'Antenna', 'RSSI', 'Frequency',
            'Hostname', 'PhaseAngle', 'DopplerFrequency'
        ]
        
        # Read the CSV with custom column names and skip the metadata
        df = pd.read_csv(file_path, skiprows=3, names=column_names)
        
        # Print the DataFrame for debugging
        print("DataFrame loaded successfully:")
        #print(df.head())

        # Ensure the 'TID' column exists
        if 'TID' not in df.columns:
            print("Error: 'TID' column not found in the file.")
            return

        # Example logic to filter team data based on 'TID' column
        team_1_tid = '1111BBBB'
        team_2_tid = '2222BBBB'

        # Seperate teams
        filtered_team_1 = df['EPC'].str.contains(team_1_tid, case=False, na=False)
        filtered_team_2 = df['EPC'].str.contains(team_2_tid, case=False, na=False)

        # Remove duplicate entries
        unique_team_1 = df[filtered_team_1].drop_duplicates(subset=['EPC'])
        unique_team_2 = df[filtered_team_2].drop_duplicates(subset=['EPC'])

        # Get number of bags in hole
        team_1_hole_count = (unique_team_1['RSSI'] > -60).sum()
        team_2_hole_count = (unique_team_2['RSSI'] > -60).sum()

        # Get number of bags on board outside of hole
        team_1_board_count = len(unique_team_1.index) - team_1_hole_count
        team_2_board_count = len(unique_team_2.index) - team_2_hole_count

        # Calculate hole points
        team_1_round_hole_score = (team_1_hole_count * 3)
        team_2_round_hole_score = (team_2_hole_count * 3)

        team_1_round_score = 0
        team_2_round_score = 0

        print(f"Team 1 Board Count = {team_1_board_count}")
        print(f"Team 1 Hole Count = {team_1_hole_count}")
        print(f"Team 2 Board Count = {team_2_board_count}")
        print(f"Team 2 hole Count = {team_2_hole_count}")

        # Scoring logic based on the counts of TID
        if team_1_board_count + team_1_round_hole_score > team_2_board_count + team_2_round_hole_score:
            team_1_round_score = (team_1_board_count + team_1_round_hole_score) - (team_2_board_count + team_2_round_hole_score)
            team_2_round_score = team_2_round_score
        elif team_2_board_count + team_2_round_hole_score > team_1_board_count + team_2_round_hole_score:
            team_2_round_score = (team_2_board_count + team_2_round_hole_score) - (team_1_board_count + team_1_round_hole_score)
            team_1_round_score = team_1_round_score

        print(f"Team 1 Round Score: {team_1_round_score}")
        print(f"Team 2 Round Score: {team_2_round_score}")

        game_scores = Ohioans_Score.GameScores()
        game_scores.update_scores(team_1_round_score, team_2_round_score)
        
    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    

