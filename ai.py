import random
# from game_object import GameObject
from player import Player
from tile import Tile
from ship import Ship
import random

class AI(Player):
  def __init__(self, difficulty, id, active):  # Constructor for GameObject class
    super().__init__(id, active) # Call parent class constructor (player.py?)
    self.difficulty = difficulty  #This is changed to 'easy', 'medium', or 'hard' during game setup
    self._moveStack = []      # stack to track possible moves from a root coordinate
    self._shotCoords = []     #This is only changed within aiTurn and will contain all shots the ai has made
    self._oppShipCoords = [] # Uhhh temporary lil variable that will need to be the list of all coordinates of enemy ships

  # Initializing board and game ====================================================  

  def locate_opp_ships(self):   # Generates a list of all enermy ship locations
    for row in range(len(self.opp.board)):
      for col in range(len(self.opp.board[row])):
        if (type(self.opp.board[row][col]) == Ship):    # Checks if the type of the current coord is a Ship
          coord = self.col_index_to_letter[col] + str(row + 1)
          self._oppShipCoords.append(coord)              # Appends the coords

  def hide_ships(self):     # Overwritten to choose random coordinates
    # Loop until all ships are hidden. Gathers the root coord for the selected ship to be oriented from.
    # ---------------------------------------------------------- #
    while self.ship_list != []: # Hide all ships
      # os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal

      self._clear_selected_ship_from_board() # Wipe invalid hide attempts. If the attempt was valid the ship would have been popped off ship_list. Otherwise it will still be the selected ship and the board will be cleaned.

      print(f"Player {self.id} - Hiding their {self.selected_ship().name}...")
      self.print_board(self.board)

      row = random.randint(0, 9)
      col = random.randint(0, 9)

      coord = self.col_index_to_letter[col] + str(row + 1)

      if self.valid_coord(coord): # If it's on the board
        if type(self.board[row][col]) == Tile: # If the targeted location is a vacant Tile
          self.__hide_ship(row, col) # Not to be confused with hide_ships(). Attempt to hide the full ship


  def __hide_ship(self, row, col):    # Overwritten to remove prints
    # Hide the selected ship
    # ---------------------------------------------------------- #
    self.__orient_ship(row, col) # orient the full length of the ship

    if self.hide_selected_ship_in_valid_location(): # place the ship if oriented in a valid position
      self.ship_list.pop(0) # Remove it from our list of remaining ships
    else:
      self.selected_ship().coords = []


  def __orient_ship(self, row, col):    # Overwritten to allow random orientation
    # If the selected ship length is > 1, orient the ship on the board while hiding it.
    # u: up
    # d: down
    # l: left
    # r: right
    # ---------------------------------------------------------- #
    # Default for 1x1 ships to orient themselves
    valid_directions = ["u","d","l","r"]
    direction = random.choice(valid_directions) if self.selected_ship_length() > 1 else "u"

    for i in range(self.selected_ship_length()):
      coords = self.direction_to_coord(direction, row, col, i)
      self.selected_ship().coords.append(coords)

  # End initializing board and game ================================================


  # Shooting functions =============================================================

  def get_input(self, message):   # Overwrites get_input from GameObject so that coordinates are returned
    return self.aiTurn()
  
  def update_sunk_ships(self, player, opponent, row, col):    # Overwrites update_sunk_ships from Player to add a clearing of _moveStack
      # Check if the opponent's ship at the attacked coordinate has been sunk
      if opponent.board[row][col].is_sunk():
          self.print_shot_result("S")
          opponent.ship_list.pop()  # Remove the sunk ship from the opponent's ship list
          self.update_board(opponent, player, row, col)  # Update the boards to show the sunk ship
          self._moveStack.clear()   # clears the stack so medium difficulty goes back to random shooting

  # End shooting functions =========================================================

  # AI decision functions ==========================================================

  def aiTurn(self):   #Function that will handle all behavior for the ai shooting, returns a valid coordinate to shoot at
    alphaCoords = ['A','B','C','D','E','F','G','H','I','J']   #Helper list of the y coord letters

    if self.aiPrevShot != 'none':                 #Check if the game has started and self.aiPrevShot is not 'none'
      self._shotCoords.append(self.aiPrevShot)    #If the game had not just started, add the value of aiPrevShot into list _shotCoords

#-----------------------------------------------START OF EASY DIFFICULTY ------------------------------------------------------------------------ 
#Get list of spaces that have been hit so far and choose a letter and number combo that has not been hit
    
    if(self.difficulty == 'easy'):  #Check if difficulty has been set to 'easy'
      
      validCoord = False                    #Var to start/stop while loop
      while not validCoord:                 #Start looping
        coord = random.choice(alphaCoords) + str(random.randint(1,10))  #Set letter and number values to random values
        
        if coord not in self._shotCoords:   #Check if the randomly selected combo has already been touched by the ai
          validCoord = True                 #If it has not been, break out of the loop
          self._shotCoords.append(coord)
      #self.aiPrevShot = coord               #Set the value of the aiPrevShot to the coord the ai found

#-----------------------------------------------START OF MEDIUM DIFFICULTY ------------------------------------------------------------------------ 
#AI will shoot randomly similar to easy mode, but will begin to shoot orthagonally once it finds a ship until it is sunk

    elif(self.difficulty == 'medium'):  #Check if the difficulty has been set to 'medium'

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

      # Updated medium with stack implementation:
      # - moveStack contains tuples containing a coordinate and directions to move from that coordinate
      # - if the stack is not empty, it will take the last item of the list (top of the stack) to get origin and possible directions
      # - it will then randomly choose from available directions and check if it is a valid direction to move
      # - if it is valid it then checks if it hits a ship in that direction it moved
      # - if it does hit, it then pushes the new coordinate on the stack and the direction it moved to get there so that it can keep moving that way
      # - each time it tests a direction it is removed from the list and once the available directions are empty it pops the entire item to backtrack
      # - whenever a ship is sunk, the entire stack is cleared
    
      if (self._moveStack):   # checks if anything is in the stack from a previous hit
        validCoord = False      # sets validCoord check to False to start loop
        while not validCoord and self._moveStack:   # loops until validCoord is found or stack is emptied
          origin = self._moveStack[-1][0] # coordinate of the shot it is shooting around
          moves = self._moveStack[-1][1]  # list of possible directions
          coord = None                    # initializes shooting coordinate

          if (not(moves)):  # checks if there are no available moves
            self._moveStack.pop()   # pops the origin and its moves off the stack

          else:             # runs if there are available moves
            direction = random.choice(moves)  # randomly chooses a direction
            self._moveStack[-1][1].remove(direction)  # removes that from the possible moves

            #----------------------------------------------UP SELECTION------------------------------------------------------
            if(direction == "u"):   #Check above the current location
              if(int(origin[1:]) > 1):  #Make sure the current location isn't the topmost position
                coord = origin[0] + str(int(origin[1:]) - 1) #If it isn't, try to hit up
            #----------------------------------------------UP SELECTION------------------------------------------------------

            #----------------------------------------------DOWN SELECTION------------------------------------------------------
            elif(direction == "d"):  #Check below the current location
              if(int(origin[1:]) < 10): #Make sure the current location isn't the bottommost position
                coord = origin[0] + str(int(origin[1:]) + 1) #If it isn't, try to hit down
            #----------------------------------------------DOWN SELECTION------------------------------------------------------

            #----------------------------------------------LEFT SELECTION------------------------------------------------------
            elif(direction == "l"):  #Check to the left of the current location
              if(origin[0].lower() != 'a'): #Make sure the current location isn't the leftmost position
                coord = alphaCoords[(alphaCoords.index(origin[0])-1)] + origin[1:] #If it isn't, try to hit to the left
            #----------------------------------------------LEFT SELECTION------------------------------------------------------

            #----------------------------------------------RIGHT SELECTION------------------------------------------------------
            elif(direction == "r"):    #Check to the right of the current location
              if(origin[0].lower() != 'j'):  #Make sure the current location isn't the rightmost position
                coord = alphaCoords[(alphaCoords.index(origin[0])+1)] + origin[1:] #If it isn't, try to hit to the right
            #----------------------------------------------RIGHT SELECTION------------------------------------------------------

            if (coord and (coord not in self._shotCoords)): #Once coord has been found, make sure it has not already been hit
                validCoord = True #If this is a valid coordinate, set validCoord to true and break out of both loops
                self._shotCoords.append(coord)
                #self.aiPrevShot = coord
        
        if not validCoord:                # runs if the stack was cleared before finding a valid target
          validCoord = False                  #Var to start/stop while loop
          while not validCoord:               #Start Looping
            coord = random.choice(alphaCoords) + str(random.randint(1,10))  #Set letter and number values to random values
            
            if coord not in self._shotCoords: #Check if the randomly selected combo has already been touched by the ai
              validCoord = True               #If it has not bee, break out of the loop
              self._shotCoords.append(coord)  # marks the coordinate as shot

              if coord in self._oppShipCoords:  # runs if the target coordinate is a ship location
                moveDirections = (coord, ["u", "d", "l", "r"])  # creates new tuple for stack with origin and all directions
                self._moveStack.append(moveDirections)          # pushes tuple onto stack
        else:
          if coord in self._oppShipCoords:    # checks if the target coordinate is a ship location
            moveDirections = (coord, [direction])   # creates new tuple with target as origin and continuing the direction
            self._moveStack.append(moveDirections)  # pushes the new origin and direction on the stack
      
      #---------------------------------------------------Random selection------------------------------------------------------
      else: 
        validCoord = False                  #Var to start/stop while loop
        while not validCoord:               #Start Looping
          coord = random.choice(alphaCoords) + str(random.randint(1,10))  #Set letter and number values to random values
          
          if coord not in self._shotCoords: #Check if the randomly selected combo has already been touched by the ai
            validCoord = True               #If it has not bee, break out of the loop
            self._shotCoords.append(coord)  # marks the coordinate as shot

            if coord in self._oppShipCoords:  # checks if the target coordinate is a ship location
              moveDirections = (coord, ["u", "d", "l", "r"])  # creates new tuple for stack with origin and all directions
              self._moveStack.append(moveDirections)          # pushes tuple onto stack
        # self.aiPrevShot = coord
      #---------------------------------------------------Random selection------------------------------------------------------
    
#-----------------------------------------------START OF HARD DIFFICULTY------------------------------------------------------------------------ 
#The ai will know the position of all ships and will hit one every turn it takes

    elif(self.difficulty == 'hard'):        #Check if the difficulty has been set to 'hard'
      coord = self._oppShipCoords.pop()  # removes ship coordinate
      
    return coord  # returns the coordinate
  
  def _aiHit(self, coord):
    #This function currently does not work, but it should be able to return true if a ship was hit, and false if it was missed
    if coord == 'none':
      return False
    
    row, col = self.coord_translator(coord)
    if isinstance(self.opp.board[row][col], Ship):
      return True
    else:
      return False

  # End AI decision functions ======================================================