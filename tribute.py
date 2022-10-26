# tales of tribute match scores
# analyzes past match outcomes and returns information to
#  improve deck selection at the start of future matches
# in a quick-to-read format.

# %%
import pandas as pd
import numpy as np

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# %%
# open spreadsheet
gc = gspread.service_account()
sh = gc.open("Tales of Tribute")

# import matches sheet
df = get_as_dataframe(sh.worksheet("matches"))

df.head()

# %% [markdown]
#

# %%
# replace nan in notes column with empty strings
df["notes"] = df["notes"].replace(np.nan, "", regex=True)

# remove any matches against NPCs or rows with missing details
df = df[df.opponent != "NPC"]
df = df.dropna()

# reset index
df.reset_index(inplace=True, drop=True)

# convert update and choice order columns to integers
df["choice"] = df["choice"].apply(int)
df["update"] = df["update"].apply(int)

# print unique values from the 'result' col to convert to number value
df.result.unique()

# %% [markdown]
# The 'notes' column is only used for occasional comments on a match
# or opponent, so NaN was replaced with empty strings for readability.
# Any matches against NPCs were removed so that deck scores reflect only
# player vs player matches. Any rows with incomplete details were also
# removed.
#
# Columns for choice order and the current update are only included for
# potential match filtering, so both were converted to integers.
#
# All unique values contained in the 'result' column were printed to convert
# match outcomes to number values.

# %%
# create new columns to hold number values for results of each match
df["won"] = 0
df["lost"] = 0

# split results column into either won or lost col
df.loc[df["result"] == "W", "won"] = 1
df.loc[df["result"] == "L", "lost"] = 1
df.loc[df["result"] == "C", "lost"] = 1


# %% [markdown]
# Two columns were created to hold number values representing match results.
# I used "C" in the match log for games where I conceded before the end of the
# match, so those were counted as losses. "DC" was used for games that were
# unfinished due to being disconnected from the game server, so I left both
# columns as 0 for those (even though technically the game registers them the
# same as conceding).

# %%
# display most recent matches
df.tail()

# %% [markdown]
# ## Scores per unique deck combination

# %%
# create new column combining all 4 decks selected per match
df["chosen decks"] = (
    df["p1 first"]
    + " "
    + df["p2 first"]
    + " "
    + df["p2 second"]
    + " "
    + df["p1 second"]
)

# sort decks in combined string alphabetically
for i, r in enumerate(df["chosen decks"]):
    chosen_decks = [deck.lower() for deck in r.split()]
    chosen_decks.sort()
    chosen_decks = (
        chosen_decks[0]
        + " "
        + chosen_decks[1]
        + " "
        + chosen_decks[2]
        + " "
        + chosen_decks[3]
    )
    df.at[i, "chosen decks"] = chosen_decks

# %% [markdown]
# Combined the four decks for each match into one string (sorted
# alphabetically) in a new column, for matching with unique deck
# combinations.

# %%
# find win & loss sums per each deck combination
lost_sum = df.groupby("chosen decks")["lost"].sum()
won_sum = df.groupby("chosen decks")["won"].sum()

# combine win & loss sums into df
deck_scores = pd.concat((won_sum, lost_sum), axis=1)

# create column of total matches per deck combination
deck_scores["total"] = deck_scores["won"] + deck_scores["lost"]

# create column of % of matches that are wins per unique combination
deck_scores["% wins"] = (deck_scores["won"] / deck_scores["total"]).round(decimals=2)

# convert to integers
deck_scores["won"] = deck_scores["won"].apply(int)
deck_scores["lost"] = deck_scores["lost"].apply(int)
deck_scores["total"] = deck_scores["total"].apply(int)

deck_scores.head(5)

# %% [markdown]
# Grouped the dataframe by the 'chosen decks' column to find the sum of
# wins and losses for each unique combination of decks. The won and lost
# columns were combined to find the total number of matches completed with
# each unique combination, and the percent of games that were won for each
# deck type was found by dividing the number of matches won by the total
# number of matches for each combination.
#
# A high success rate means less with fewer matches played, so being able to
# see both the total and success rate is helpful when deciding which deck to
# choose.

# %%
# import txt of all deck combinations
all_combos = pd.read_csv("combinations.txt", names=["a", "b", "c", "d"])

# make sure all decks are lowercase
all_combos["a"] = all_combos["a"].str.lower()
all_combos["b"] = all_combos["b"].str.lower()
all_combos["c"] = all_combos["c"].str.lower()
all_combos["d"] = all_combos["d"].str.lower()

# combine decks in new column (they're already be in alphabetical order)
all_combos["chosen decks"] = (
    all_combos["a"]
    + " "
    + all_combos["b"]
    + " "
    + all_combos["c"]
    + " "
    + all_combos["d"]
)

# put decks column before individual deck choice columns
all_combos = all_combos[["chosen decks", "a", "b", "c", "d"]]

all_combos.head(5)

# %% [markdown]
# Pulled a list of all possible unique combinations from a text file. After making sure they were all lowercase, the values from the four separate columns were combined into one 'chosen decks' column to match up with the deck_scores dataframe. The combinations sheet already has the decks in alphabetical order, so they should already match up with the decks df without sorting.

# %%
# left merge deck_scores onto df of all deck combinations
combos = all_combos.merge(
    deck_scores, how="left", left_on="chosen decks", right_index=True
)

combos.head(5)

# %% [markdown]
# Merged the deck_scores dataframe with the all_combos dataframe, to make sure unused deck combinations (like the first two rows) were included.

# %%
# fill any blanks from unused combinations with 0s or blanks
combos.fillna({"won": 0, "lost": 0, "total": 0}, inplace=True)

# %% [markdown]
# Filled in missing values for unused deck combinations. The '% wins' column was left unchanged to avoid reading a deck combination with zero matches total for a combination with 100% losses.

# %%
# move choesen decks to end before sending to google sheets
combos = combos[["a", "b", "c", "d", "won", "lost", "total", "% wins", "chosen decks"]]

# update sheet with current combo results
worksheet = sh.worksheet("scoresdf")

set_with_dataframe(worksheet, combos)
print("scoresdf updated")

# %% [markdown]
# Updated the scoresdf sheet with the result sums for the unique deck combinations in the combos dataframe.

# %% [markdown]
# ## Opponent deck choice patterns
#
# At the start of each match, player 1 chooses one deck, followed by player 2 choosing 2 decks. Player 1 then gets to choose the final deck. Some deck combinations tend to have results more sensitive to RNG/"luck of the draw", and having the chance to choose the final deck can mean avoiding those combinations (and any others I struggle with). The list of wins and losses per deck combination is enough for making the last choice as player 1, but it's difficult as player 2 to figure out which two decks will be safest alongside whatever player 1 chooses. For example, if player 1 chooses blue, I might choose black and yellow. Of the remaining options for the final deck, green means a combination I've won 60% of the time, orange means a combination I've won 65% of the time, and orgnum or red would mean combinations I've won with at least 50%+. But if they choose purple, it's probably not going to go well: I've only won 1 out of 4 games with the black, blue, purple, and yellow decks. If I knew in advance they were going to choose purple for the final deck, I wouldn't pick black and yellow.
#
#  While most players don't have much of a noticeable pattern to their choices, some players choose the same two decks no matter what decks I choose, even if I've won against them several games in a row with those four decks in some cases. Being able to quickly see if the other player has an obvious pattern to their past choices can help avoid a match I'm more likely to lose.

# %%
# create new columns
for col in ("op deck 1", "op deck 2"):
    df[col] = ""

# fill new columns based on choice order
for i, r in enumerate(df["choice"]):
    if r == 1:
        # fill new cols for matches as player 1
        df.at[i, "op deck 1"] = df.at[i, "p2 first"]
        df.at[i, "op deck 2"] = df.at[i, "p2 second"]

    if r == 2:
        # fill new cols for matches as player 2
        df.at[i, "op deck 1"] = df.at[i, "p1 first"]
        df.at[i, "op deck 2"] = df.at[i, "p1 second"]

# %% [markdown]
# Created new columns for the opposing player's deck choices in each match. The new column values are taken from either the p1 or p2 first and second columns, depending on the value in the choice order column. Only the opponent's deck choices are saved.

# %%
# filter dataframe for opposing player sheet
player_df = df[
    [
        "opponent",
        "op deck 1",
        "op deck 2",
        "won",
        "lost",
        "notes",
    ]
]

# sort matches by opponent username
player_df = player_df.sort_values(by="opponent", key=lambda col: col.str.lower())

# reset index
player_df.reset_index(drop=True, inplace=True)

# %%
# set worksheet to save player_df to
worksheet = sh.worksheet("players")

# save worksheet to Google Sheets
set_with_dataframe(worksheet, player_df)
print("players worksheet updated")

# %%
# create a list of all individual decks from the combos df
keys = np.unique(combos[["a", "b", "c", "d"]].values)

# create an empty dictionary to hold the mean success rates
single_decks = {}

for key in keys:
    # find all chosen deck combinations containing an individual deck
    filtered_games = combos[combos["chosen decks"].str.contains(key, na=False)]
    # find the mean success rate with combinations including that deck
    single_decks[key] = filtered_games["% wins"].mean()

# print the mean success rate for each individual deck
for key, value in single_decks.items():
    print(str("{}: {:.2f}".format(key, value)))
