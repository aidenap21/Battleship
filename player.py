from game_object import GameObject
from tile import Tile
from ship import Ship

class Player(GameObject):
  def __init__(self, id, active):
    super().__init__()
    self.id = id
    self.active = active #boolean
    self.board = []
    self.__build_board_of_tiles(self.board)
    self.attacked_coords = []
    self.ship_list = []

    # Opponent information
    self.opp = None # The other Player
    self.opps_board = [] # Board to track where you have fired at your opponent
    self.__build_board_of_tiles(self.opps_board)

  def set_opponent(self,opponent):
    self.opp = opponent

  def __build_board_of_tiles(self, board):
    # Fills out a given list with 10 nested lists of 10 Tile items
    # ---------------------------------------------------------- #
    for row in range(10):
      board.append([]) # add row
      for col in range(10):
        tile = Tile(row, col)
        board[row].append(tile) # place tiles

  def set_ship_list(self, num_ships):
    # Add the proper number of properly sized ships to self.ship_list. Ship(name, size, symbol)
    # ---------------------------------------------------------- #
    self.ship_list = [
      Ship(
        self.ship_size_to_name[f"1x{i}"],  # Ship name (e.g. "Destroyer")
        f"1x{i}",                          # Ship size (e.g. "1x3")
        self.ship_size_to_symbol[f"1x{i}"] # Ship symbol (e.g. "#")
      )
      for i in range(1, num_ships + 1)
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

  def __clear_selected_ship_from_board(self):
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
      self.__clear_selected_ship_from_board() # Wipe invalid hide attempts. If the attempt was valid the ship would have been popped off ship_list. Otherwise it will still be the selected ship and the board will be cleaned.

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

  def attack_ship(self, coord):
    # need a boalean return for this so we can mark the opponents board when a hit(true)
    row, col = self.coord_translator(coord)
    self.hit(coord) if isinstance(self.opp.board[row][col], Ship) else  self.miss(coord)

  def hit(self, coord):
    row, col = self.coord_translator(coord)
    self.mark_shot(self.opps_board, coord, "H") # Hit your opponent's ship. Tracking it for yourself.
    self.mark_shot(self.opp.board, coord, "H") # Hit your opponent's ship. Update their board
    self.opp.board[row][col].hp -= 1 # Decrement opponent's ship health
    self.update_sunk_ships(self, self.opp, coord)

  def miss(self, coord):
    self.mark_shot(self.opps_board, coord, "M") # Missed your opponent's ship. Tracking it for yourself.
    self.mark_shot(self.opp.board, coord, "M") # Missed your opponent's ship. Update their board

  def mark_shot(self, board, coord, result):
    row, col = self.coord_translator(coord)
    obj = board[row][col] # Either a Tile or Ship
    if isinstance(obj, Ship):
      for tile in obj.tiles: # for literal Tile in the selected Ship.tiles
        if tile.row == row and tile.col == col: # if the coordinates to be marked match the Tile's coordinates
          obj = tile

    obj.symbol = result

    if board == self.opps_board: # Mark shot is called twice per hit/miss, so we only want to print the result once
      self.print_shot_result(result)

  def print_shot_result(self, result):
    self.br()
    self.br(result, gap = 5)

  def update_board(self, sinking_player, other_player, row, col):
    for tile in sinking_player.board[row][col].tiles:
      other_player.opps_board[tile.row][tile.col].symbol = "S"
      sinking_player.board[tile.row][tile.col].sink()

  def update_sunk_ships(self, player, opponent, coord):
    row, col = self.coord_translator(coord)

    # Check if the opponent's ship is sunk
    if opponent.board[row][col].is_sunk():
      opponent.ship_list.pop()
      self.update_board(opponent, player, row, col)

    # Check if the player's ship is sunk
    elif player.board[row][col].is_sunk():
      player.ship_list.pop()
      self.update_board(player, opponent, row, col)

  def print_ship_list(self):
    # Print the ship list
    # ---------------------------------------------------------- #
    for ship in self.ship_list:
      print(f"{ship.name} ({ship.size})")

  def print_remaining_ships_to_hide(self):
    if self.ship_list != []:
      print("\nRemaining ships:")
      self.print_ship_list()