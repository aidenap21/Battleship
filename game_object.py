"""
  Program Name: GameObject
  
  Description: GameObject provides  functions to handle the game. It has method 
  for validating coordinates, printing the game board, translating coordinates,
  and handling game inputs

  Inputs: 
  -Coordinates 
  -Board object
  -User inputs for checking if the player wants to quit

  Output:
  -print the game board
  -select hit/miss/sink/win phrases based on game events
  -Translated coordinates
  Author: 
  Jaxon Avena

  Creation Date: 
  September 10, 2024
"""

import random  # Import the random module for random selections
from ship import Ship  # Import the Ship class from the ship module

class GameObject:  # Define the GameObject class
  def __init__(self):  # Constructor for GameObject class
    # Dictionary mapping ship sizes to ship names
    self.ship_size_to_name = {
      "1x1": "Cruiser",  # 1x1 ship is called Cruiser
      "1x2": "Submarine",  # 1x2 ship is called Submarine
      "1x3": "Destroyer",  # 1x3 ship is called Destroyer
      "1x4": "Battleship",  # 1x4 ship is called Battleship
      "1x5": "Aircraft Carrier"  # 1x5 ship is called Aircraft Carrier
    }
    # Dictionary mapping ship sizes to ship symbols
    self.ship_size_to_symbol = {
      "1x1": "&",  # Symbol for 1x1 ship is &
      "1x2": "%",  # Symbol for 1x2 ship is %
      "1x3": "#",  # Symbol for 1x3 ship is #
      "1x4": "$",  # Symbol for 1x4 ship is $
      "1x5": "@"  # Symbol for 1x5 ship is @
    }
    # Dictionary mapping column letters to indices (0-9)
    self.letter_to_col_index = {
      "A": 0,  # Column A corresponds to index 0
      "B": 1,  # Column B corresponds to index 1
      "C": 2,  # Column C corresponds to index 2
      "D": 3,  # Column D corresponds to index 3
      "E": 4,  # Column E corresponds to index 4
      "F": 5,  # Column F corresponds to index 5
      "G": 6,  # Column G corresponds to index 6
      "H": 7,  # Column H corresponds to index 7
      "I": 8,  # Column I corresponds to index 8
      "J": 9  # Column J corresponds to index 9
    }

    # Dictionary mapping column letters to indices (0-9)
    self.col_index_to_letter = {
      0: "A",  # Column A corresponds to index 0
      1: "B",  # Column B corresponds to index 1
      2: "C",  # Column C corresponds to index 2
      3: "D",  # Column D corresponds to index 3
      4: "E",  # Column E corresponds to index 4
      5: "F",  # Column F corresponds to index 5
      6: "G",  # Column G corresponds to index 6
      7: "H",  # Column H corresponds to index 7
      8: "I",  # Column I corresponds to index 8
      9: "J"  # Column J corresponds to index 9
    }

    # List of hit phrases to randomly select from
    self.hit_syns = ["Hit!", "!!! H I T !!!", "BANNNNNNNNNNNGGGGGGGG!", "Bullseye!", "Noiiiiiiiceeee one mate"]
    # List of miss phrases to randomly select from
    self.miss_syns = ["Miss!", "You missed.", "L", "oof", "Go fish?", "BLOCKED BY JAMES!!!"]
    # List of sink phrases to randomly select from
    self.sink_syns = ["Nice Sink!"]
    # List of win phrases to randomly select from
    self.win_syns = ["Sweet Victory!", "Winner! Winner! Chicken Dinner!", "congrats bro", "Might be the Greatest", "Proved Me Wrong"]

    # Dictionary to map result characters to corresponding phrases lists
    self.syns = {
      "M": self.miss_syns,  # "M" corresponds to miss phrases
      "H": self.hit_syns,  # "H" corresponds to hit phrases
      "S": self.sink_syns,  # "S" corresponds to sink phrases
      "W": self.win_syns  # "W" corresponds to win phrases
    }

  # Method to print a breakline of a specified character
  def br(self, char="=", gap=0):
    # If char is H, M, S, or W, select a corresponding phrase
    char = (self.synonymizer_inator(char) if char in ["H", "M", "S", "W"] else char) + (" " * gap)
    # Print a line of 50 characters with gaps
    print("\n" + (char * 50) + "\n")

  # Method to select a random synonym from the lists
  def synonymizer_inator(self, char):
    return random.choice(self.syns[char])  # Return a random choice from the corresponding phrase list

  # Method to check if a given coordinate is valid
  def valid_coord(self, coord):
    try:
      # Extract the column letter and convert to uppercase
      col = coord[0].upper()
      # Extract the row number and convert to integer
      row = int(coord[1:])
    except:
      # If extraction fails, print an error message and return False
      print("Your coordinate must be a letter-number pair (e.g. A8)")
      return False

    # Check if the column letter is valid (A-J)
    if col not in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
      print("Invalid Coordinate. Ensure your input starts with a valid column header (e.g. E4)")
      return False

    # Check if the row number is valid (1-10)
    if row not in range(1, 11):
      print("Invalid Coordinate. Ensure your input lies within the bounds of the 10x10 board.")
      return False

    return True  # If all checks pass, return True

  # Method to check if all coordinates in a list are within bounds
  def coords_are_inbounds(self, coords):
    # Loop through each coordinate in the list
    for coord in coords:
      # Check if the row and column are within 0-9
      if coord[0] > 9 or coord[0] < 0 or coord[1] > 9 or coord[1] < 0:
        return False  # Return False if any coord is out of bounds
    return True  # Return True if all coordinates are in bounds

  # Method to translate a coordinate like A8 to row and column indices
  def coord_translator(self, coord):
    # Convert column letter to index
    col = self.letter_to_col_index[coord[0].upper()]
    # Convert row number to index (subtract 1 for zero-based indexing)
    row = int(coord[1:]) - 1
    # Return row and column as indices
    return row, col

  # Method to print the board with rows and columns labeled
  def print_board(self, board):
    # Print the column headers
    print("   A B C D E F G H I J")
    row = 0  # Initialize row counter
    # Loop through each row in the board
    for row_list in board:
      stringified_objs = []  # Initialize a list to store symbols
      col = 0  # Initialize column counter
      # Loop through each object in the row
      for obj in row_list:
        # Check if the object is a Ship
        if isinstance(obj, Ship):
          # Loop through each tile in the ship's tiles list
          for tile in obj.tiles:
            # If the current tile's row and column match the current row and column
            if tile.row == row and tile.col == col:
              obj = tile  # Set the object to the tile
        col += 1  # Increment the column counter
        # Add the object's symbol to the list of stringified objects
        stringified_objs.append(obj.symbol)
      # Print the row number and the symbols for that row
      extra_space = " " if row != 9 else ""
      print(f"{row + 1} " + extra_space + " ".join(stringified_objs))
      row += 1  # Increment the row counter

  # Method to check if the user wants to quit the game
  def quit(self, input):
    # If the input matches any quit command
    if input in ["exit", "q", "quit", "EXIT", "Q", "QUIT"]:
      exit()  # Exit the program

  # Method to get input from the user and check for quit commands
  def get_input(self, message):
    my_input = input(message)  # Get user input with a message prompt

    self.quit(my_input)  # Call quit() method to check if the user wants to quit
    return my_input  # Return the user's input