# Fantasy Football Draft Analyzer 2024
## The purpose of this application is to analyze a 2024 fantasy football draft.

### Setup
For this application, no setup is necessary other than cloning or forking the repo. 

### How it works
This application grades fantasy drafts based on predicted ADP from sources BeatADP (source here: https://www.beatadp.com/platform-adp/sleeper) and Sleeper's API (source here: https://docs.sleeper.com/). Using predicted ADP along with the position a player was drafted in, I created an algorithm that calculates a player's draft grade based on their deviation from their predicted spot. The overall grade is based on the average grade of all individual players drafted.

### How to use
The application is fairly straightforward to use. When opening the folder, please navigate to the "run_me.py" file. After opening it, you will be greeted with this screen.
![image](https://github.com/user-attachments/assets/ea61c87b-086f-48ec-af0e-a7708d8c06d7)
Please navigate to this button in the top right and click.
![image](https://github.com/user-attachments/assets/cbd5aaff-b7f3-4230-bb19-c35d16e06647)

After running, a window will pop up that looks like this. ![image](https://github.com/user-attachments/assets/a5473a03-4885-4f81-8976-dc21039ce21d)

In this window users can adjust settings to their league. 
Currently, there are only three options available in terms of scoring: _standard, half-ppr, and full-ppr_

## Steps for using the application
1. Adjust sliders to settings.
2. Type in scoring type for the league (standard, half ppr, full ppr). These **MUST BE EXACT**. Nothing needs to be pressed after inputting the scoring type. If no league scoring format is inputted, the application will default to standard scoring.
3. Click "Generate Draft Positions". This will generate your draft positions depending on what position your first pick is.
4. Proceed to input a player's name and click on "Draft Player". The name needs to be spelled out, so nicknames unfortunately do not work. However, with players that have a "Jr.", etc. attached to the end of their name, this can be omitted. For names containing punctuation (A.J. Brown), please type these. Once you have drafted a player, text will appear in the text box below saying what player was drafted.
![image](https://github.com/user-attachments/assets/f8e18c8f-3fbc-4576-9353-28fa49893c0d)
###### This is what everything should look like once settings have been adjusted and players have been drafted.
5. Once all players have been drafted, the text box will display a few lines of text. In this text will be analysis about the draft, including best picks, biggest reaches, what your predicted draft was and finally what your draft grade was.
![image](https://github.com/user-attachments/assets/0fbdde37-1977-47ab-9b55-7fb98b42aa75)
###### This is what the draft analysis should look like

If you get an error message saying that the player couldn't be drafted, this means that the player's name was not inputted correctly. The application will stay at the same pick so feel free to keep trying to draft the player with different spellings of names.

### Possible errors and caveats
Currently, there is no implementation of nicknames or different spellings of names (as evidenced by the omission of Jr.) and no other scoring options such as a 2 QB or dynasty leagues. These are all things I wanted to implement but couldn't figure out or didn't have time for. There is also no current implementation for Kicker or Defense/Special Teams ratings, as both of these were omitted from the APIs and files that I found. I tried to figure out a way to implement them to no avail, but with a different API this may be possible to implement.

## Thank you for using this application and enjoy!
