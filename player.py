"""
Program Name: BattleShip Player

Description: This file defines the player class which inherits from the GameObject class. it tracks 
the attacks of each player, update the game board, and setting up te opponent's information. It also manage
the hiding of ships, checking for hits or misses, and determining if the ship has been sunk. 

Inputs:
    - Player ID(whether the player is active or not).
    - User inputs for placing ships on the board and attacking opponent coordinates.
    - Coordinates for translating attacks and ship placements.
    - Number of ships per player.

Output:
    - Prints the player and opponent boards, updates the boards after attacks, and 
      displays the results of hits, misses, or ship sinking.


Author:
    Jaxon Avena

Creation Date:
    September 10, 2024
"""

from game_object import GameObject # Import the GameObject class from game_object module
from tile import Tile  # Import the Tile class from tile module
from ship import Ship # Import the Ship class from ship module
import os

class Player(GameObject):
  def __init__(self, id, active):  # Constructor for Player class
    super().__init__()  # Call the parent class constructor
    self.id = id  # Set the player's ID
    self.active = active  # Set whether the player is active (True/False)
    self.board = []  # Initialize an empty list for the player's board
    self.__build_board_of_tiles(self.board)  # Build the player's board by calling __build_board_of_tiles
    self.attacked_coords = []  # Initialize an empty list for attacked coordinates
    self.ship_list = []  # Initialize an empty list for the player's ships
    self.super_shot = True 

    # Opponent information
    self.opp = None # The other Player
    self.opps_board = [] # Board to track where you have fired at your opponent
    self.__build_board_of_tiles(self.opps_board) # Build the opponent's board by calling __build_board_of_tiles

  # Method to set the opponent for the player
  def set_opponent(self, opponent):
    self.opp = opponent  # Set the opponent to the passed player object

  def __build_board_of_tiles(self, board):
    # Fills out a given list with 10 nested lists of 10 Tile items
    # ---------------------------------------------------------- #
    for row in range(10):
      board.append([]) # add row
      for col in range(10): # Loop through columns 0-9
        tile = Tile(row, col) # Create a new Tile object for each row and column
        board[row].append(tile) # place tiles

  # Method to set the list of ships for the player
  def set_ship_list(self, num_ships):
    # Add the proper number of properly sized ships to self.ship_list. Ship(name, size, symbol)
    # ---------------------------------------------------------- #
    self.ship_list = [
      Ship(
        self.ship_size_to_name[f"1x{i}"],  # Ship name (e.g. "Destroyer")
        f"1x{i}",                          # Ship size (e.g. "1x3")
        self.ship_size_to_symbol[f"1x{i}"] # Ship symbol (e.g. "#")
      )
      for i in range(1, num_ships + 1) # Loop from 1 to num_ships
    ]
    self.ship_list.reverse() # Desc. order

  def selected_ship(self):
    # Return the ship that is currently selected, AKA at the front of self.ship_list
    # ---------------------------------------------------------- #
    return self.ship_list[0]

  def selected_ship_length(self):
    # Return the length of the selected ship. (e.g. The length of a 1x3 ship is 3)
    # ---------------------------------------------------------- #
    return int(self.selected_ship().size[-1])

  def _clear_selected_ship_from_board(self):
    # Restore the initial ship placement to be a Tile.
    # ---------------------------------------------------------- #
    for row in range(10):
      for col in range(10):
        if self.board[row][col] == self.selected_ship():
          self.board[row][col] = Tile(row, col)
    self.selected_ship().tiles = []

  def hide_ships(self):
    # Loop until all ships are hidden. Gathers the root coord for the selected ship to be oriented from.
    # ---------------------------------------------------------- #
    while self.ship_list != []: # Hide all ships
      os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal

      self._clear_selected_ship_from_board() # Wipe invalid hide attempts. If the attempt was valid the ship would have been popped off ship_list. Otherwise it will still be the selected ship and the board will be cleaned.

      print(f"Player {self.id} - Hiding their {self.selected_ship().name}...")
      self.print_board(self.board)

      coord = self.get_input("Hide the ship: ")

      if self.valid_coord(coord): # If it's on the board
        row, col = self.coord_translator(coord)
        if type(self.board[row][col]) == Tile: # If the targeted location is a vacant Tile
          self.__hide_ship(row, col) # Not to be confused with hide_ships(). Attempt to hide the full ship

  def __hide_ship(self, row, col):
    # Hide the selected ship
    # ---------------------------------------------------------- #
    self.__orient_ship(row, col) # orient the full length of the ship

    if self.hide_selected_ship_in_valid_location(): # place the ship if oriented in a valid position
      self.ship_list.pop(0) # Remove it from our list of remaining ships
    else:
      print("You cannot place your ship out of bounds or over another ship. Try again.")
      self.selected_ship().coords = []

    self.print_remaining_ships_to_hide()

  def __orient_ship(self, row, col):
    # If the selected ship length is > 1, orient the ship on the board while hiding it.
    # u: up
    # d: down
    # l: left
    # r: right
    # ---------------------------------------------------------- #
    # Default for 1x1 ships to orient themselves
    direction = self.__select_direction() if self.selected_ship_length() > 1 else "u"

    if direction in ["u","d","l","r"]: # Extra check
      for i in range(self.selected_ship_length()):
        coords = self.direction_to_coord(direction, row, col, i)
        self.selected_ship().coords.append(coords)
    else:
      print("Pick one: u d l r")

  def __select_direction(self):
    direction = "" # Init for while loop
    while direction not in ["u","d","l","r"]:
      print("u = Up\nd = Down\nl = Left\nr = Right")
      direction = input("Which direction do you want your ship to be oriented?: ").lower()

    return direction

  def hide_selected_ship_in_valid_location(self):
    # Verify if the selected ship's list of coordinates are all on the board and vacant Tiles
    # ---------------------------------------------------------- #
    flag = False
    if self.coords_are_inbounds(self.selected_ship().coords): # if we're at least trying to place the ship on the board...
      for coord in self.selected_ship().coords:
        tile = self.board[coord[0]][coord[1]]
        if type(tile) == Tile: #...make sure we're not overlapping ships
          # Append the tile that the ship is replacing into the Ship.tiles list to track its unique symbol and coords
          tile.symbol = self.selected_ship().symbol
          self.selected_ship().tiles.append(tile)
          self.board[coord[0]][coord[1]] = self.selected_ship() # Set the Tile's location on the board to be the Ship
          flag = True
        else:
          return False # Every coord needs to be a vacant tile`
    else:
      self.selected_ship().coords = [] # We're going to retry hiding the ship if we're out of bounds, so we wipe the ship's coords list
    return flag

  def direction_to_coord(self, direction, row, col, i):
    # Translate up, down, left, or right in relation to a coordinate into the new coordinate corresponding with the direction.
    # ---------------------------------------------------------- #
    direction_to_coord = {
      "u": [row - i, col],
      "d": [row + i, col],
      "l": [row, col - i],
      "r": [row, col + i]
    }
    return direction_to_coord[direction]

  def attack_ship(self, coord, super_shot):
    # need a boalean return for this so we can mark the opponents board when a hit(true)
    row, col = self.coord_translator(coord)
    if super_shot:            # checks if super shot was passed in as true
      self.super_shoot(row, col)    # calls super shot function
    else:                     # normal shot
      self.hit(row, col) if isinstance(self.opp.board[row][col], Ship) else self.miss(row, col)
                              # checks if position is a ship and marks a hit or miss otherwise

  def hit(self, row, col):
    self.mark_shot(self.opps_board, row, col, "H") # Hit your opponent's ship. Tracking it for yourself.
    self.mark_shot(self.opp.board, row, col, "H") # Hit your opponent's ship. Update their board
    self.opp.board[row][col].hp -= 1 # Decrement opponent's ship health
    self.update_sunk_ships(self, self.opp, row, col)

  def super_shoot(self, row, col): # performs a 3x3 super shot
    for r in range(row - 1, row + 2):     # iterates through rows to shoot in the super shot
      if r < 0 or r > 9:                    # checks if the current row is off the board and passes
        continue
      for c in range(col - 1, col + 2):     # iterates through cols to shoot in the super shot
        if c < 0 or c > 9:                    # checks if the current col is off the board and passes
          continue
        coord = self.col_index_to_letter[col] + str(row + 1)  # converts the row and col back to string coordinates
        if coord not in self.attacked_coords:     # checks  if the current coord has already been shot or not
          if isinstance(self.opp.board[r][c], Ship):  # checks if it hits in the current spot
            self.hit(r, c)                              # calls hit function to mark accordingly
          else:                                       # missed shot
            self.miss(r, c)                             # calls miss function to mark accordingly

  def miss(self, row, col):
    self.mark_shot(self.opps_board, row, col, "M") # Missed your opponent's ship. Tracking it for yourself.
    self.mark_shot(self.opp.board, row, col, "M") # Missed your opponent's ship. Update their board

  def mark_shot(self, board, row, col, result):
    obj = board[row][col] # Either a Tile or Ship
    if isinstance(obj, Ship):
      for tile in obj.tiles: # for literal Tile in the selected Ship.tiles
        if tile.row == row and tile.col == col: # if the coordinates to be marked match the Tile's coordinates
          obj = tile

    obj.symbol = result

    if board == self.opps_board: # Mark shot is called twice per hit/miss, so we only want to print the result once
      self.print_shot_result(result)

  # Method to print the result of a shot (hit or miss)
  def print_shot_result(self, result):
      self.br()  # Print a breakline to separate sections for better readability
      self.br(result, gap = 5)  # Print the result of the shot (hit or miss) with a gap between characters

  # Method to update the boards when a ship is sunk
  def update_board(self, sinking_player, other_player, row, col):
      # Loop through each tile of the sinking ship
      for tile in sinking_player.board[row][col].tiles:
          # Update the opponent's board to show that the ship has been sunk (mark with "S")
          other_player.opps_board[tile.row][tile.col].symbol = "S"
          # Call the sink() method on the ship to mark its tiles as sunk on the sinking player's board
          sinking_player.board[tile.row][tile.col].sink()

  # Method to update the game state when ships are sunk
  def update_sunk_ships(self, player, opponent, row, col):
      # Check if the opponent's ship at the attacked coordinate has been sunk
      if opponent.board[row][col].is_sunk():
          self.print_shot_result("S")
          opponent.ship_list.pop()  # Remove the sunk ship from the opponent's ship list
          self.update_board(opponent, player, row, col)  # Update the boards to show the sunk ship

      # Check if the player's own ship at the attacked coordinate has been sunk
      elif player.board[row][col].is_sunk():
          player.ship_list.pop()  # Remove the sunk ship from the player's ship list
          self.update_board(player, opponent, row, col)  # Update the boards to show the sunk ship

  # Method to print the list of ships for the player
  def print_ship_list(self):
      # Loop through each ship in the player's ship list and print its name and size
      for ship in self.ship_list:
          print(f"{ship.name} ({ship.size})")

  # Method to print the remaining ships that need to be hidden
  def print_remaining_ships_to_hide(self):
      if self.ship_list != []:  # Check if there are still ships to hide
          print("\nRemaining ships:")  # Print a message indicating that there are remaining ships
          self.print_ship_list()  # Call print_ship_list() to display the list of remaining ships
