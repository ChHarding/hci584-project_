# General Description
- The purpose of this project is to create an application that will analyze the user's fantasy football draft for the season. 
- The application will have a screen where users can choose to either import their drafts automatically or manually. If imported manually, users will be able to adjust all settings (scoring, number of players, number of teams, etc.) to the numbers according to their league. After, users will be asked questions based on their drafts ("was ____ available at this spot in the draft?" etc.) in order for the algorithm to better understand draft grades.
- After importing their draft and answering all questions, users will receive a draft grade and analysis on what the draft could have improved in or what went well. Users can also click on players to see what players could have been better at the position. 
- The application will use the Sleeper fantasy API as an external mechanism in order to access fantasy football data as well as individual player statistics and draft predictions. Using the Sleeper API also allows the user to import their own fantasy draft if their league uses Sleeper, bypassing the need to manually import any settings.
- This application could use a minimal CLI, but ideally I would use a GUI that has some sort of visual indicator. This application will use the Tkinter library already integrated within Python to create a GUI that will display all the necessary information.
- If users want to save their draft grade results, they can also choose to save the draft as a PNG file.

# Task Vignettes
1. User input
   - Richard just drafted his fantasy football team for the season in his league with his high school friends. He's worried that he will lose because he had very little confidence in the players he drafted. The league has a $50 buyin and he also would really like the money. He downloads the fantasy football draft analyzer application to see how he did compared to what was predicted for him. He is greeted with two options on the GUI: one to import his draft manually and the other automatically through Sleeper. His league is on ESPN so he realizes he has to manually update all the settings. He chooses manual, then is greeted by a screen with rule changes. He changes all relevant settings to what the league uses, then clicks on "next" to find his screen full with players. He chooses where he drafted all of his players, and upon completion is asked a couple yes or no questions about what players were available when he drafted other players. He receives a draft grade after completion, and is intrigued to find out that he scored a B+. He then scrolls through the results, which give him a comprehensive overview of his draft along with draft analyses at certain positions. He then saves the draft results as an image to look at later.
   Details for later:
     - Probably need a preset for each grade for a comprehensive draft report, otherwise I would have to implement AI to create one which might be too difficult.
     - Have to make sure to take out already drafted players, otherwise user can choose the same player at multiple positions.
     - Maybe want to implement more options for different league types...? Best ball vs. H2H vs. dynasty, etc.
     - # EDIT # pictures will be difficult to import so I have decided on not implementing pictures for now. This will be added if I have enough time. League types will also be dependent on if I can find a way to adjust scoring with previously imported players.
2. Automatic roster
   - Richard sends the application to a friend who just drafted on Sleeper. His friend uses the application but instead imports his own league and draft settings through Sleeper. Questions were still asked based on player positions when drafting, but the process was significantly faster.

# Technical Flow
- All fantasy football data regardless of what host application the user uses will be pulled from the Sleeper API:  https://docs.sleeper.com/
- User input (choosing what players were drafted) will be used as part of a query. Each time the user inputs a new player, a new query is performed.
- Query will return as strings and images that the user can save into a PNG if they wish.
- Each player will have an analysis taken from the Sleeper API while the comprehensive review will be hard coded based on what grade is chosen for the draft.
- Draft grades will be given based on the deviation from ADP, with a draft that is exact to the predicted ADP being average.
- # EDIT # this will be dependent on the API I decide to use. Current Sleeper API doesn't provide this information outright for me so I have to do some searching.
- # EDIT # unfortunately, I do not think importing drafts automatically will be available as I cannot seem to find a way to do it within Sleeper.
