from itertools import combinations

# default deck names
deck_list = ["black", "blue", "green", "orange", "orgnum", "purple", "red", "yellow"]

# confirm deck names to use for combinations list
# deck names should match names used in google sheets log

while True:

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
        if len(deck_list) != 8:
            print("\nERROR: must enter 8 deck names.\n")

    elif choice == "Y":

        # create a list of unique combinations of decks per match

        deck_combinations = list()
        deck_combinations = [
            ",".join(map(str, comb)) for comb in combinations(deck_list, 4)
        ]
        print("All combinations:\n", deck_combinations)

        # save deck combinations to use with tribute.ipynb
        with open("combinations.txt", "w") as cmb:
            for item in deck_combinations:
                cmb.write("%s\n" % item)

        print("\nDeck Combinations saved.")
        break

    elif choice == "Q":
        # quit
        break

    else:
        print("Invalid choice.")
