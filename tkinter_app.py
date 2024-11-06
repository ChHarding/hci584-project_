import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import json

class DraftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fantasy League Draft")
        self.geometry("450x460")

        self.player_dict = self.read_players("players.json")
        self.user_draft = []
        self.draft_positions = []
        self.x = 0

        self.create_widgets()

    def create_widgets(self):
        # League Size
        self.league_size_label = ttk.Label(self, text="League Size:")
        self.league_size_label.grid(row=0, column=0, padx=10, pady=10)
        self.league_size = tk.IntVar(value=10)
        self.league_size_slider = ttk.Scale(self, from_=2, to=20, orient='horizontal', variable=self.league_size, command=self.update_league_size_label)
        self.league_size_slider.grid(row=0, column=1, padx=10, pady=10)
        self.league_size_value_label = ttk.Label(self, text=str(self.league_size.get()))
        self.league_size_value_label.grid(row=0, column=2, padx=10, pady=10)

        # Team Size
        self.team_size_label = ttk.Label(self, text="Team Size:")
        self.team_size_label.grid(row=1, column=0, padx=10, pady=10)
        self.team_size = tk.IntVar(value=15)
        self.team_size_slider = ttk.Scale(self, from_=2, to=30, orient='horizontal', variable=self.team_size, command=self.update_team_size_label)
        self.team_size_slider.grid(row=1, column=1, padx=10, pady=10)
        self.team_size_value_label = ttk.Label(self, text=str(self.team_size.get()))
        self.team_size_value_label.grid(row=1, column=2, padx=10, pady=10)

        # First Pick Position
        self.position_label = ttk.Label(self, text="First Pick Position:")
        self.position_label.grid(row=2, column=0, padx=10, pady=10)
        self.position = tk.IntVar(value=1)
        self.position_slider = ttk.Scale(self, from_=1, to=20, orient='horizontal', variable=self.position, command=self.update_position_label)
        self.position_slider.grid(row=2, column=1, padx=10, pady=10)
        self.position_value_label = ttk.Label(self, text=str(self.position.get()))
        self.position_value_label.grid(row=2, column=2, padx=10, pady=10)

        # Generate Draft Positions Button
        self.generate_button = ttk.Button(self, text="Generate Draft Positions", command=self.generate_draft_positions)
        self.generate_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Player Name Entry
        self.player_name_label = ttk.Label(self, text="Player Name:")
        self.player_name_label.grid(row=4, column=0, padx=10, pady=10)
        self.player_name = tk.StringVar()
        self.player_name_entry = ttk.Entry(self, textvariable=self.player_name)
        self.player_name_entry.grid(row=4, column=1, padx=10, pady=10)

        # Draft Player Button
        self.draft_button = ttk.Button(self, text="Draft Player 1 of 1", command=self.draft_player)
        self.draft_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Draft Status (ScrolledText)
        self.draft_status = ScrolledText(self, wrap=tk.WORD, width=50, height=10)
        self.draft_status.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def update_league_size_label(self, event):
        self.league_size_value_label.config(text=str(self.league_size.get()))

    def update_team_size_label(self, event):
        self.team_size_value_label.config(text=str(self.team_size.get()))

    def update_position_label(self, event):
        self.position_value_label.config(text=str(self.position.get()))

    def draft(self, player_name):
        '''finds player and add to list of user's players
        params: player_name (string)
                player_dict (dict)
                user_draft (list)
        returns: user_draft
        '''
        found_player = False
        for key in self.player_dict: # looking for player by iterating through dictionary
            player = self.player_dict[key]
            full_name = (player['first_name'] + " " + player['last_name']).lower()
            if full_name == player_name.lower(): # player is only appended if name in dictionary is same
                self.user_draft.append(player)
                found_player = True

        if found_player == False: # returns false if player not found
            return False
        else:
            return True

    def calculate_grade(self):
        '''
        def calculate_grade calculates draft grade by predicted ranking

        params: user_draft (list): list of players user has drafted
                draft_positions (list): list of positions user is drafting in
        returns: predicted_score (int): the predicted score based on draft positions
                 score (int): the actual score based on drafted players
                 grade (string): letter grade assigned to value
        '''

        predicted_score = sum(self.draft_positions)

        score = sum(player['search_rank'] for player in self.user_draft)

        if score <= predicted_score - 75:
            grade = "S"
        elif score <= predicted_score - 50:
            grade = "A"
        elif score <= predicted_score - 25:
            grade = "B"
        elif score <= predicted_score or score <= predicted_score + 25:
            grade = "C"
        elif score <= predicted_score + 50:
            grade = "D"
        else:
            grade = "F"

        return predicted_score, score, grade

    def read_players(self, filename):
        '''def read_players reads in players into json file

        params: filename (string): filename to read
        returns: player_dict (dictionary): dictionary with all players
        '''
        with open(filename , "r") as fo:
            player_dict = json.load(fo) 
        return player_dict

    def predicted_spots(self, position, league_size, team_size):
        '''def predicted_spots returns all predicted draft spots the user will draft at
        
        params: position (string): position that player's first pick is
                league_size (string): number of people in the league
                team_size (string): number of players on each team
        '''
        draft_order = [] # list for all picks
        current_pick = int(position) # starting at the first pick
        
        for round_number in range(int(team_size)):
            if round_number % 2 == 0: # regular order for odd rounds
                current_round = list(range(1, int(league_size) + 1))
            else: # reverse order for even rounds (snake draft)
                current_round = list(range(int(league_size), 0, -1))
            
            # calculate total pick number
            draft_order.append(current_pick + current_round[int(position) - 1] - 1)
            current_pick += int(league_size)
        
        return draft_order

    def generate_draft_positions(self):
        league_size = self.league_size.get()
        team_size = self.team_size.get()
        position = self.position.get()
        self.draft_positions = self.predicted_spots(position, league_size, team_size)
        self.draft_status.insert(tk.END, f"Draft positions: {self.draft_positions}\n")
        self.draft_button.config(text=f"Draft Player 1 of {team_size}")

    def draft_player(self):
        player_name = self.player_name.get()
        if self.x < len(self.draft_positions):
            success = self.draft(player_name)
            if not success:
                self.draft_status.insert(tk.END, "Try again!\n")
            else:
                self.draft_status.insert(tk.END, f"You have drafted {player_name}\n")
                self.x += 1
                self.player_name.set('')  # Clear the input field
                if self.x >= len(self.draft_positions):
                    predicted_score, score, grade = self.calculate_grade()
                    self.draft_status.insert(tk.END, f"Draft complete! Predicted score: {predicted_score}, Actual score: {score}, Grade: {grade}\n")
                else:
                    self.draft_button.config(text=f"Draft Player {self.x + 1} of {len(self.draft_positions)}")

if __name__ == "__main__":
    app = DraftApp()
    app.mainloop()