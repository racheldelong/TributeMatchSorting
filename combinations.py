# tales of tribute deck combinations
# creates a csv of all unique combinations to use with tribute.ipynb

from itertools import combinations
from tkinter import Y

# default deck names
deck_list = ["black", "blue", "green", "orange", "orgnum", "purple", "red", "yellow"]

# total number of decks currently in game
total_decks = 8

while True:

    # confirm deck names to use for combinations list
    # deck names should match names used in google sheets log

    # print deck names to use for combinations.txt
    print("Deck names:", deck_list)
    choice = input("Enter 'Y' to use, 'N' to change, or 'Q' to quit.\n")

    if choice == "N":

        # get user's preferred deck names
        # ex: 'Duke of Crows' might be 'purple', 'duke', 'crow', etc

        deck_string = input(
            "Enter deck names used in match log, separated by commas:\n"
        )

        # separate input into list items
        deck_list = deck_string.split(",")

        # check that all deck names were entered
        if len(deck_list) != total_decks:
            print("\nERROR: must enter {} deck names.\n".format(total_decks))

    elif choice == "Y":

        # create list of unique combinations of 4 decks per match
        deck_combinations = list()
        deck_combinations = [
            ",".join(map(str, comb)) for comb in combinations(deck_list, 4)
        ]
        print("All combinations:\n", deck_combinations)

        # save match deck combinations
        with open("combinations.txt", "w") as cmb:
            for item in deck_combinations:
                cmb.write("%s\n" % item)
            print("Deck Combinations (4) saved to 'combinations.txt'")

        # create list of unique combinations of 3 decks for choice chart
        deck_combinations = list()
        deck_combinations = [
            ",".join(map(str, comb)) for comb in combinations(deck_list, 3)
        ]

        # save match deck combinations
        with open("choice.txt", "w") as cmb:
            for item in deck_combinations:
                cmb.write("%s\n" % item)
            print("Deck Combinations (3) saved to 'cmb3.txt'")
            print("Done")
        break

    elif choice == "Q":
        # quit
        print("Done")
        break

    else:
        print("Invalid choice.")
