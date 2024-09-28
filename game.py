"""
Program Name: Game Manager

Description: This file defines the Game class which inherits from GameObject. It manages
the flow of the Battleship game, including swicthing player turns, setting up board, and 
determining  when the game ends. it aslo allow players to attack coordinates, set the number
set the number of ships, and print the current state of the game

Inputs:
    - player_bank = [p1, p2]
    - User inputs for setting the number of ships and choosing attack coordinates.

Output:
    - Displays the current turn, player boards, and the results of attacks (hit/miss).
    - Declares the winner when the game ends.

Author:
    Jaxon Avena

Creation Date:
    September 10, 2024
"""

from game_object import GameObject  # Import the GameObject class from game_object module
from player import Player
import time
import os

class Game(GameObject):  # Define the Game class, inheriting from GameObject
  def __init__(self, player_bank):  # Constructor for Game class
    super().__init__()  # Call the parent class constructor
    self.player_bank = player_bank  # Set player_bank to the passed value
    self.player1 = player_bank[0]  # Set player1 to the first player in player_bank
    self.player2 = player_bank[1]  # Set player2 to the second player in player_bank
    self.turn_count = 1  # Initialize turn_count to 1
    self.active_player = self.get_active_player()  # Get the active player
    self.num_ships = 0  # Initialize num_ships to 0

  # Method to switch turns between players
  def __switch_turns(self):
    # Loop through each player in player_bank
    for player in self.player_bank:
      player.active = (not player.active)  # Toggle the active status of each player
    self.active_player = self.get_active_player()  # Update the active player

  # Method to start the game
  def start(self):
    self.__get_num_ships()  # Get the number of ships each player will have
    self.__set_ship_lists()  # Set the ship lists for each player
    self.__setup_boards()  # Set up the boards and hide the ships

    self.__set_ship_lists()  # Regenerate the ship lists for the game
    self.__take_turn(1)  # Start the game by taking the first turn

  # Method to take a turn
  def __take_turn(self, turn_count):
    # Check if the active player's ship list is empty (game over)
    if self.active_player.ship_list == []:
      self.end_game()  # End the game

    if (type(self.active_player) == Player):  # only prints for player type and not AI
      print(f"\n ==== Round #{turn_count} ==== Player {self.active_player.id}'s turn ====\n")  # Print the current turn number and active player
      print("Your board")  # Print player's own board
      self.print_board(self.active_player.board)  # Call print_board() to display active player's board
      print("Opp's board")  # Print opponent's board
      self.print_board(self.active_player.opps_board)  # Call print_board() to display the opponent's board

    coord = self.active_player.get_input(f"Player {self.active_player.id} -- Attack a coordinate: ")  # Prompt the active player for a coordinate to attack
    super_shot = False

    if (coord[-1].lower() == 's'):              # check for super shot flag
      coord = coord[:-1]                           # remove the flag from the coord string
      if self.active_player.super_shot:           # checks if super shot has already been used by the player
        self.active_player.super_shot = False       # sets flag to False to mark that it has now been used
        super_shot = True

    os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal

    # If the input is a valid coordinate
    if self.valid_coord(coord):
      # Check if the coordinate has already been attacked
      if coord not in self.active_player.attacked_coords:
        self.active_player.attacked_coords.append(coord)  # Add the coordinate to the list of attacked coordinates
        self.active_player.attack_ship(coord, super_shot)  # Call attack_ship() to attack the ship at the coordinate
        if (type(self.active_player) == Player):  # only prints for player type and not AI
          print("=" * 50)  # Print a separator line
        self.turn_count += 1  # Increment the turn count
      else:
        print("Space already taken. Try again!")  # If the spot has already been attacked, print an error message

    if (type(self.active_player) == Player):  # only prints for player type and not AI
      print("Your board")  # Print player's own board
      self.print_board(self.active_player.board)  # Call print_board() to display active player's board
      print("Opp's board")  # Print opponent's board
      self.print_board(self.active_player.opps_board)  # Call print_board() to display the opponent's board
      self.br()
      print("Pass the screen to the next player")

    if (type(self.player2) == Player):  # doesn't wait when playing against AI
      time.sleep(8)
    os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal

    self.__switch_turns()  # Switch turns to the other player
    self.__take_turn(self.turn_count)  # Call __take_turn() recursively to continue the game

  # Method to get the active player
  def get_active_player(self):
    # Loop through each player in the player_bank
    for player in self.player_bank:
      if player.active == True:  # If the player is active
        return player  # Return the active player

  # Method to set up the boards for both players
  def __setup_boards(self):
    # Loop through each player in player_bank
    for player in self.player_bank:
      player.hide_ships()  # Call hide_ships() for each player to hide their ships
      os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal
      print(f"Player {player.id} - All ships are hidden...")  # Print that all ships are hidden
      self.print_board(player.board)  # Print the player's board after ships are hidden
      self.br()  # Print a break line

      if (type(self.player2) == Player):  # doesn't wait when playing against AI
        print("Pass the screen to the next player")
        time.sleep(5)
      os.system('cls' if os.name == 'nt' else 'clear')

  # Method to get the number of ships from the user
  def __get_num_ships(self):
    # Keep asking for the number of ships until a valid number (1-5) is entered
    while 0 >= self.num_ships or self.num_ships > 5:
      print("Please enter a number between 1 and 5.")  # Prompt the user to enter a number between 1 and 5
      try:
        self.num_ships = int(input("How many ships per team?: "))  # Convert the input to an integer
      except:
        self.num_ships = 0  # If an error occurs, set num_ships to 0

  # Method to set the ship lists for both players
  def __set_ship_lists(self):
    self.player1.set_ship_list(self.num_ships)  # Set the ship list for player1
    self.player2.set_ship_list(self.num_ships)  # Set the ship list for player2

  # Method to end the game
  def end_game(self):
    self.br()  # Print a break line
    self.br("W", gap = 5)  # Print a victory message
    self.br()  # Print another break line
    print(f"Player {self.active_player.opp.id} wins!")  # Print the winning player's ID
    exit()  # Exit the program