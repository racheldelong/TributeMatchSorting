# Tales of Tribute Match Sorting

For my Code Kentucky Data Analysis 2 project, I'm creating a Jupyter notebook to analyze a record of match details and outcomes from *The Elder Scrolls Online's* Tales of Tribute (ToT) deck-building card game. Each match starts with players taking turns choosing four decks, with thirty seconds for each choice. Player 1 chooses the first deck to start, followed by player 2 choosing the second and third decks. Player 1 then chooses the final deck. The combination of decks in a game can have a significant impact on the outcome. Most players are more comfortable with particular combinations and have an easier time winning with them, but might fail to notice if their favorites are weak when combined in specific ways. It's also important to make sure that there are multiple ways to win with the decks chosen for a match--some combinations come down to luck of the draw significantly more often than others, with fewer options for recovering once you fall behind.

----------
__Objective:__ analyze past match outcomes and return information to inform deck selection at the start of future matches in a quick-to-read format.

----------

## Project Plan

__Feature 1:__ A worksheet will be read in from Google Sheets using the gspread API, and merged with a text file of all unique deck combinations. A program to build the list of combinations will be included, to add future decks or change the preferred label for each deck.

__Feature 2:__ Find the success rate of the deck combinations found in the match log, and merge with the dataframe of all deck combinations. Decks in each row of the match dataframe will be rearranged in alphabetical order to find success rates for each unique combination, regardless of the order they were chosen.

__Feature 3:__ Create matplotlib bar graphs showing the performance of unique deck combinations containing an individual deck for the lowest performing decks to visualize combinations that should be avoided or that require more practice.

__Feature 4:__ Use a conda environment and include instructions for setup.