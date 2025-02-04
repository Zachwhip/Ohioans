# Ohioans_Score.py

import Ohioans_File
import Ohioans_UI

class GameScores:
    def __init__(self):
        #self.team_1_score = 0
        #self.team_2_score = 0
        self.game_started = False   # Track whether the game has started

    def start_game(self):
        if not self.game_started:
            self.game_started = True    # Set the flag to true when the game starts
            print("Game Started! Scores reset to 0.")
        else:
            print("Game already started. Scores will not be reset again until the program is stopped and started again.")
    
    def stop_game(self):
        if self.game_started:
            print("Game stopped. Scores will not be reset until started again.")
            self.game_started = False   # Reset the game_started flag when the game stops
        else:
            print("Game is already stopped.")

    def update_scores(self, team_1_round_score, team_2_round_score):
        # Update total scores with the new round scores
        #self.team_1_score += team_1_round_score
        #self.team_2_score += team_2_round_score
        #print(f"Updated Scores - Team 1: {self.team_1_score}, Team 2: {self.team_2_score}")
        # Ohioans_File.team_1_score 
        # Ohioans_File.team_2_score
        Ohioans_File.team_1_score += team_1_round_score
        Ohioans_File.team_2_score += team_2_round_score
        print(f"Updated Scores - Team 1: {Ohioans_File.team_1_score}, Team 2: {Ohioans_File.team_2_score}")

    def get_scores(self):
        return self.team_1_score, self.team_2_score
    
    def print_scores(self):
        print(f"Current Scores - Team 1: {self.team_1_score}, Team 2: {self.team_2_score}")