import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import json
from pprint import pprint
import json
import csv

class DraftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fantasy League Draft")
        self.geometry("500x600")

        self.player_dict = self.read_players("players.json")
        self.user_draft = []
        self.draft_positions = []

        self.standard_json = self.csv_to_json("beatadp_standard_combined__sleeper_rankings.csv", "standard.json")
        self.half_ppr_json = self.csv_to_json("beatadp_halfppr_combined__sleeper_rankings.csv", "half ppr.json")
        self.full_ppr_json = self.csv_to_json("beatadp_ppr_combined__sleeper_rankings.csv", "full ppr.json")
        self.standard = self.read_players("standard.json")
        self.half_ppr = self.read_players("half ppr.json")
        self.full_ppr = self.read_players("full ppr.json")

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

        # League Type Entry
        self.league_type_label = ttk.Label(self, text="League Type:")
        self.league_type_label.grid(row=3, column=0, padx=10, pady=10)
        self.league_type = tk.StringVar()
        self.league_type_entry = ttk.Entry(self, textvariable=self.league_type)
        self.league_type_entry.grid(row=3, column=1, padx=10, pady=10)

        # Generate Draft Positions Button
        self.generate_button = ttk.Button(self, text="Generate Draft Positions", command=self.generate_draft_positions)
        self.generate_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Player Name Entry
        self.player_name_label = ttk.Label(self, text="Player Name:")
        self.player_name_label.grid(row=5, column=0, padx=10, pady=10)
        self.player_name = tk.StringVar()
        self.player_name_entry = ttk.Entry(self, textvariable=self.player_name)
        self.player_name_entry.grid(row=5, column=1, padx=10, pady=10)

        # Draft Player Button
        self.draft_button = ttk.Button(self, text="Draft Player 1 of 1", command=self.draft_player)
        self.draft_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        # Draft Status (ScrolledText)
        self.draft_status = ScrolledText(self, wrap=tk.WORD, width=50, height=15)
        self.draft_status.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def update_league_size_label(self, event):
        self.league_size_value_label.config(text=str(self.league_size.get()))

    def update_team_size_label(self, event):
        self.team_size_value_label.config(text=str(self.team_size.get()))

    def update_position_label(self, event):
        self.position_value_label.config(text=str(self.position.get()))

    def draft(self, player_name):
        '''
        def draft finds player and add to list of user's players

        params: player_name (string)
        returns: True if player was drafted, false if player not found
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
        
    def rate_score(self, grade_num, league_size):
        '''
        def rate_score gives grade to score for individual draft pick

        params: grade_num (int or float)
                league_size (int)
        returns: grade (string) based on calculation
        '''

        if grade_num <= -1 * (int(league_size)):
            return "S"
        elif grade_num <= -0.6 * (int(league_size)) and grade_num > -1 * (int(league_size)):
            return "A"
        elif grade_num <= -0.2 * (int(league_size)) and grade_num > -0.6 * (int(league_size)):
            return "B"
        elif grade_num > -0.2 * (int(league_size)) and grade_num <= 0.2 * (int(league_size)):
            return "C"
        elif grade_num <= 0.6 * (int(league_size)) and grade_num > 0.2 * (int(league_size)):
            return "D"
        else:
            return "F"
        
    def calculate_grade(self, league_size, team_size, league_type="standard"):
        '''
        def calculate_grade calculates draft grade by predicted ranking

        params: league_type (string): scoring type for league
                team_size (int): number of players on team
                league_size (string): 
        returns: grade (string): letter grade assigned to value, prints predicted score and your score as well
        '''
        if league_type == "standard":
            scoring = self.standard
        elif league_type == "half ppr":
            scoring = self.half_ppr
        else:
            scoring = self.full_ppr

        # predicted score + draft, rankings and names in separate lists for later
        draft_predictions = self.predicted_draft(league_type) # no need for if statements because predicted_draft has if statements built in
        predicted_rankings = []
        predicted_names = []
        user_rankings = []
        user_names = []
        deviations = []
        rated_picks = []

        for x in range(int(team_size)):
            # predicted draft
            predicted_rankings.append(int(draft_predictions[x]['Rank']))
            predicted_names.append(draft_predictions[x]['Player'])

            # user draft
            for player in scoring:
                full_name = (self.user_draft[x]['first_name'] + " " + self.user_draft[x]['last_name']).lower()
                if full_name == player['Player'].lower():
                    user_names.append(player['Player'])
                    user_rankings.append(int(player['Rank']))

            # calculate deviations, individual pick grades between each player
            temp_dev = int(user_rankings[x]) - int(predicted_rankings[x])
            deviations.append(temp_dev)
            rated_picks.append(self.rate_score(temp_dev, int(league_size)))

        # find best and worst picks and average pick deviation
        biggest_reach = max(deviations)
        best_pick = min(deviations)
        avg_dev = sum(deviations) / int(team_size)
        #print(avg_dev)
        #print(biggest_reach, best_pick)

        # store and return pick deviations, players involved, grade
        biggest_reach_index = deviations.index(max(deviations))
        best_pick_index = deviations.index(min(deviations))
        biggest_reach_between = [predicted_names[biggest_reach_index], user_names[biggest_reach_index]]
        best_pick_between = [predicted_names[best_pick_index], user_names[best_pick_index]]
        grade = self.rate_score(avg_dev, int(league_size))
        #print(biggest_reach_between)
        #print(best_pick_between)

        return best_pick, best_pick_between, best_pick_index, biggest_reach, biggest_reach_between, biggest_reach_index, draft_predictions, grade
    
    def csv_to_json(self, csv_filename, json_filename):
        '''
        def csv_to_json converts csv files to json
        
        params: csv_filename (string): filename to read
                json_filename (string): filename to save to
        returns: json_filename (string): filename saved to
        '''
        # Read the CSV file
        with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
                
            # Convert rows to a list of dictionaries
            data = [row for row in csv_reader]

        # Write data to a JSON file
        with open(json_filename, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

        return json_filename

    def read_players(self, filename):
        '''
        def read_players reads in players into json file

        params: filename (string): filename to read
        returns: player_dict (dictionary): dictionary with all players
        '''
        with open(filename , "r") as fo:
            player_dict = json.load(fo) 
        return player_dict

    def predicted_spots(self, position, league_size, team_size):
        '''
        def predicted_spots returns all predicted draft spots the user will draft at
        
        params: position (string): position that player's first pick is
                league_size (string): number of people in the league
                team_size (string): number of players on each team
        returns: draft_order (list of int)
        '''
        draft_order = [] # list for all picks
        current_pick = int(position) # starting at the first pick
        
        for round_number in range(int(team_size)):
            if round_number % 2 == 0: # regular order for odd rounds
                current_round = list(range(1, int(league_size) + 1))
            else: # reverse order for even rounds (snake draft)
                current_round = list(range(league_size, 0, -1))
            
            # calculate total pick number
            draft_order.append(current_pick + current_round[int(position) - 1] - 1)
            current_pick += int(league_size)
        
        return draft_order
    
    def predicted_draft(self, league_type):
        '''
        def predicted_draft uses draft positions to create draft of predicted players

        params: league_type (string): rankings for players depends on scoring type
        returns: predicted (list of dictionaries): list of players' ranks and names
        '''
        predicted = []

        if league_type == "standard":
            for spot in self.draft_positions:
                spot_str = str(spot)
                for player in self.standard:
                    if player.get('Rank') == spot_str:
                        predicted.append(player)
                        continue
        elif league_type == "half ppr":
            for spot in self.draft_positions:
                spot_str = str(spot)
                for player in self.half_ppr:
                    if player.get('Rank') == spot_str:
                        predicted.append(player)
                        continue
        else:
            for spot in self.draft_positions:
                spot_str = str(spot)
                for player in self.full_ppr:
                    if player.get('Rank') == spot_str:
                        predicted.append(player)
                        continue

        return predicted

    def generate_draft_positions(self):
        league_size = self.league_size.get()
        team_size = self.team_size.get()
        position = self.position.get()
        self.draft_positions = self.predicted_spots(position, league_size, team_size)
        self.draft_status.insert(tk.END, f"Draft positions: {self.draft_positions}\n")
        self.draft_button.config(text=f"Draft Player 1 of {team_size}")

    def draft_player(self):
        player_name = self.player_name.get()
        league_size = self.league_size.get()
        team_size = self.team_size.get()
        league_type = self.league_type.get()
        if self.x < len(self.draft_positions):
            success = self.draft(player_name)
            if not success:
                self.draft_status.insert(tk.END, "Try again!\n")
            else:
                self.draft_status.insert(tk.END, f"You have drafted {player_name} at pick number {self.draft_positions[self.x]}.\n")
                self.x += 1
                self.player_name.set('')  # Clear the input field
                if self.x >= len(self.draft_positions):
                    best_pick, best_pick_between, best_pick_index, biggest_reach, biggest_reach_between, biggest_reach_index, draft_predictions, grade = self.calculate_grade(league_size, team_size, league_type)
                    self.draft_status.insert(tk.END, f"Draft complete! Your grade was: {grade}.\n")
                    self.draft_status.insert(tk.END, f"Your best pick was at pick {self.draft_positions[best_pick_index]}. Your predicted pick was {best_pick_between[0]} but you picked {best_pick_between[1]}. It was the best pick by {abs(best_pick)} spots.\n")
                    self.draft_status.insert(tk.END, f"Your biggest reach was at pick {self.draft_positions[biggest_reach_index]}. Your predicted pick was {biggest_reach_between[0]} but you picked {biggest_reach_between[1]}. It was the best pick by {biggest_reach} spots.\n")
                    self.draft_status.insert(tk.END, f"Your predicted draft was: {draft_predictions}\n")
                else:
                    self.draft_button.config(text=f"Draft Player {self.x + 1} of {len(self.draft_positions)}")

if __name__ == "__main__":
    app = DraftApp()
    app.mainloop()