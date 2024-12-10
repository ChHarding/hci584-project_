# Developer Documentation

## Overview
This is an application that will grade a user's fantasy football draft. Users will adjust settings and input players and will receive 
a draft analysis of their picks afterwards. It uses Sleeper's API (link found in user guide) and BeatADP's player rankings (also found in user guide)
to rank players on predicted ADP. It uses an algorithm based on number of teams, players and deviation at draft spot vs. ADP to give the user a score
and analysis of their draft.

## Final Planning Specs
### Currently implemented:
- Drafting players
- League setting customization
- League scoring types (standard, half ppr, full ppr)
- Basic GUI through Tkinter

## User Interaction
### Basic flow:
For basic flow, users will open the application and adjust settings to be in line with their league. 
![image](https://github.com/user-attachments/assets/3da2e295-9f0c-4060-9f39-94e99312d552)

Afterwards, users will input a number of players and press draftin order to add them to their team, with confirmation of the player being drafted
 found in the text box below. 
 
![image](https://github.com/user-attachments/assets/547b2f74-248d-4df9-b3be-a5759f5b3cdb)

Users will then receive a draft analysis in the text box below as well.
![image](https://github.com/user-attachments/assets/5587d471-2e45-4225-a1c5-03be0c750230)

### Step-by-step:
1. Users will first adjust the settings of the application to be in line with their league. This will just adjust self values in the run_me.py file.
2. Users will then type in what type of scoring they use for their league (also adjusting a self value).
3. Users then click on the "Generate Draft Positions" button to generate what draft positions they would have drafted in (generate_draft_positions > predicted_spots())
4. Once users have done this, they will then draft the players by inputting a player name and pressing "Draft Player" (draft_player() > draft())
5. After inputting all players, users will receive a draft analysis detailing their results (calculate_grade() > predicted_draft > rate_score())

### Other methods
Other methods are read_players() and csv_to_json(). csv_to_json() takes all content from a csv file and transfers it to a json file. read_players() takes input
from a json file and rewrites it as a dictionary.

## Known Issues
### Minor issues
The main minor issue would be the exclusion of league scoring type. This has been worked around by creating a default scoring type (standard) but I imagine could be 
fixed by creating some sort of button or checkbox. Could not figure out for the life of me how to implement it so I created a workaround, which is why this is 
only a minor issue.

### Major issues
The main major issue would be if a user drafts a kicker or defense/special teams. These two positions do not have ranks, ratings or scores attached to them but can be
found in the Sleeper API, making them draft-able. I suspect that this will create a major runtime exception in the calculate_grade() method and could be fixed if
the two positions were able to be omitted but would leave out functionality. Instead, I would rather have this fixed by either switching APIs to one that includes
the two positions or to find another list that includes them.

## Future Work
Throughout this project there were a lot of things I was ambitious in doing but was unable to accomplish. The biggest thing would be including pictures of players 
and having some sort of animation for grades. I didn't have time to implement this but want more visual "pop" in the future. I also wanted to add Sleeper league 
integration but couldn't figure out how to import the draft of a player specifically. I found another package off Reddit that someone created (found in the first 
cell of the Jupyter notebook) but also couldn't figure out how to use it. I also couldn't implement defense and kicker ratings (as stated before) so users are
unable to get the full experience of drafting an entire fantasy team. Lastly, I want to be able to use this application over multiple years. However, in its current
state that would mean manually inputting new rankings from BeatADP each year instead of finding a package. I found that ESPN's API possibly has this integration but 
by that point it was too late to switch APIs.
