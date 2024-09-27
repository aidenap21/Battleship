import random
from game_object import GameObject
from tile import Tile
from ship import Ship

class AI(GameObject):
  def __init__(self, difficulty, id, active):  # Constructor for GameObject class
    self.difficulty = difficulty  #This is changed to 'easy', 'medium', or 'hard' during game setup
    self.aiPrevShot = 'none'  #This is only changed within aiTurn and will hold the last shot the ai made
    self.aiHitCoords = []     #This is only changed within aiTurn and will contain all shots the ai has made
    self.originalHit = ''     #Set whenever ai hits a ship for the first time
    self.sameShip = False     #Lock originalHit until a ship is sunk
    self.randomMoves = []     #List that contains the possibile random moves. Each move gets removed after test

    self.tempShipList = [] # Uhhh temporary lil variable that will need to be the list of all coordinates of enemy ships

    # Stuff yoinked from player class:
    super().__init__() # Call parent class constructor (game_object.py?)
    self.id = id # Set AI's ID to 2
    self.active = active # Set player active boolean
    self.board = [] # Init empty board list
    self.__build_board_of_tiles(self.board) # Build board
    self.opp = None # Will be set by main to Player 1
    self.opps_board = [] # Init empty board list
    self.__build_board_of_tiles(self.opps_board) # Build board
    self.attacked_coords = [] # Init empty attacked coords list
    self.ship_list = [] # Init empty ship list

  # Initializing board and game ====================================================  

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
  
  def __clear_selected_ship_from_board(self):
    # Restore the initial ship placement to be a Tile.
    # ---------------------------------------------------------- #
    for row in range(10):
      for col in range(10):
        if self.board[row][col] == self.selected_ship():
          self.board[row][col] = Tile(row, col)
    self.selected_ship().tiles = []

  def hide_ships(self):
    print("TODO")
    '''
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
    '''
  
  def __hide_ship(self, row, col):
    print("TODO")
    '''
    # Hide the selected ship
    # ---------------------------------------------------------- #
    self.__orient_ship(row, col) # orient the full length of the ship

    if self.hide_selected_ship_in_valid_location(): # place the ship if oriented in a valid position
      self.ship_list.pop(0) # Remove it from our list of remaining ships
    else:
      print("You cannot place your ship out of bounds or over another ship. Try again.")
      self.selected_ship().coords = []

    self.print_remaining_ships_to_hide()
    '''

  def __orient_ship(self, row, col):
    '''
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
    '''

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

  # End initializing board and game ================================================

  # Shooting functions =============================================================

  def attack_ship(self, coord):

    # need a boalean return for this so we can mark the opponents board when a hit(true)
    row, col = self.coord_translator(coord)
    if coord[-1].lower() == 's' and self.super_shot:      # add super shot code here
      self.super_shot = False
    #   self.super_hit
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

  def update_board(self, sinking_player, other_player, row, col):
    # Loop through each tile of the sinking ship
    for tile in sinking_player.board[row][col].tiles:
        # Update the opponent's board to show that the ship has been sunk (mark with "S")
        other_player.opps_board[tile.row][tile.col].symbol = "S"
        # Call the sink() method on the ship to mark its tiles as sunk on the sinking player's board
        sinking_player.board[tile.row][tile.col].sink()

  # Method to update the game state when ships are sunk
  def update_sunk_ships(self, player, opponent, coord):
      row, col = self.coord_translator(coord)  # Translate the attacked coordinate into row and column indices

      # Check if the opponent's ship at the attacked coordinate has been sunk
      if opponent.board[row][col].is_sunk():
          self.print_shot_result("S")
          opponent.ship_list.pop()  # Remove the sunk ship from the opponent's ship list
          self.update_board(opponent, player, row, col)  # Update the boards to show the sunk ship

      # Check if the player's own ship at the attacked coordinate has been sunk
      elif player.board[row][col].is_sunk():
          player.ship_list.pop()  # Remove the sunk ship from the player's ship list
          self.update_board(player, opponent, row, col)  # Update the boards to show the sunk ship

  # End shooting functions =========================================================

  # AI decision functions ==========================================================

  def aiTurn(self):
    alphaCoords = ['a','b','c','d','e','f','g','h','i','j']

    if self.aiPrevShot != 'none':
      self.aiHitCoords.append(self.aiPrevShot)
    
    if(self.difficulty == 'easy'):
      #Get list of spaces that have been hit so far and choose a letter and number combo that has not been hit
      
      validCoord = False
      while not validCoord:
        coord = random.choice(alphaCoords) + str(random.randint(1,10))
        if coord not in self.aiHitCoords:
          validCoord = True
      self.aiPrevShot = coord

    elif(self.difficulty == 'medium'):
      #if previous shot was a hit, attempt to shoot in one of the 4 orthagonal directions UNTIL ship is sunk 

      #This one sucks but heres my thought process:
      # -At the start of the game randomly shoot
      # -Keep randomly shooting until a hit is detected
      # -At this point, save the coordinate that the first hit was detected, and lock it until that ship is destroyed
      # -Randomly shoot orthagonally until another hit is made
      # -Repeat cycle until it reaches the end, although this may need some additional subcases:
      #     - What if another ship is put at the end of the ship the ai is currently attacking?
      #     - What if there is another ship that is put to the side of the ship the ai is attacking?
      # -Other than those cases, if the ai reaches the end there is 2 options:
      #     - The ship is sunk: continue on randomly hitting spaces
      #     - The ship is not sunk: return to the original hit and keep randomly choosing a direction until another hit is made
      # -Once a ship is sunk, reset the sameShip flag to signify the ai is moving on 
    
      if(self.aiPrevShot != 'none' or self._aiHit(self.aiPrevShot) == True): # If first shot or hit on last shot
        if(self.sameShip == False): # If not the same ship
          self.originalHit = self.aiPrevShot # ??
          self.sameShip = True # Set

        while(not(validCoord))
          if(not(self.randomMoves)):
            #start back from first hit part of ship and continue from there
            self.aiPrevShot = self.originalHit
            
            
          validCoord = False
          self.randomMoves = [0,1,2,3]
          while(not(validCoord) and (self.randomMoves)):
            
            nextShot = random.choose(self.randomMoves) #0-right, 1-left, 2-down, 3-up

            if nextShot == 0:
              if(alphaCoords[alphaCoords.index(self.aiPrevShot[0])] != 'j'):
                coord = alphaCoords[(alphaCoords.index(self.aiPrevShot[0])+1)] + self.aiPrevShot[1]
              self.randomMoves.remove(0)

            elif(nextShot == 1):
              if(alphaCoords[alphaCoords.index(self.aiPrevShot[0])] != 'a'):
                coord = alphaCoords[(alphaCoords.index(self.aiPrevShot[0])-1)] + self.aiPrevShot[1]
              self.randomMoves.remove(1)

            elif(nextShot == 2):
              if(int(self.aiPrevShot[1]) < 10):
                coord = self.aiPrevShot[0] + str(int(self.aiPrevShot[1]) + 1)
              self.randomMoves.remove(2)

            else:
              if(int(self.aiPrevShot[1]) > 1):
                coord = self.aiPrevShot[0] + str(int(self.aiPrevShot[1]) - 1)
              self.randomMoves.remove(3)

            if coord not in self.aiHitCoords:
                validCoord = True
                self.aiPrevShot = coord

      else:
        validCoord = False
        while not validCoord:
          coord = random.choice(alphaCoords) + str(random.randint(1,10))
          if coord not in self.aiHitCoords:
            validCoord = True
        self.aiPrevShot = coord

    
    elif(self.difficulty == 'hard'):
      #Get coords of all ships in the list and iterate thru all of them
      if(not(self.aiHitCoords)):
        coord = self.tempShipCoordsList[0]
      else:
        coord = self.tempShipCoordsList(self.tempShipList.index(self.aiPrevShot) + 1)
      self.aiPrevShot = coord

    return coord
  
  def _aiHit(self, coord):
    #This function currently does not work, but it should be able to return true if a ship was hit, and false if it was missed
    row, col = self.coord_translator(coord)
    if isinstance(self.opp.board[row][col], Ship):
      return True
    else:
      return False

  # End AI decision functions ======================================================