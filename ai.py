import random
# from game_object import GameObject
from player import Player
from tile import Tile
from ship import Ship
import random

class AI(Player):
  def __init__(self, difficulty, id, active):  # Constructor for GameObject class
    self.difficulty = difficulty  #This is changed to 'easy', 'medium', or 'hard' during game setup
    self.aiPrevShot = 'none'  #This is only changed within aiTurn and will hold the last shot the ai made
    self.aiHitCoords = []     #This is only changed within aiTurn and will contain all shots the ai has made
    self.originalHit = ''     #Set whenever ai hits a ship for the first time
    self.sameShip = False     #Lock originalHit until a ship is sunk
    self.randomMoves = []     #List that contains the possibile random moves. Each move gets removed after test

    self.tempShipList = [] # Uhhh temporary lil variable that will need to be the list of all coordinates of enemy ships
    super().__init__(id, active) # Call parent class constructor (game_object.py?)

  # Initializing board and game ====================================================  

  def hide_ships(self):     # Overwritten to choose random coordinates
    # Loop until all ships are hidden. Gathers the root coord for the selected ship to be oriented from.
    # ---------------------------------------------------------- #
    while self.ship_list != []: # Hide all ships
      # os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal

      self.__clear_selected_ship_from_board() # Wipe invalid hide attempts. If the attempt was valid the ship would have been popped off ship_list. Otherwise it will still be the selected ship and the board will be cleaned.

      # print(f"Player {self.id} - Hiding their {self.selected_ship().name}...")
      # self.print_board(self.board)

      row = random.randint(0, 9)
      col = random.randint(0, 9)

      coord = self.col_index_to_letter[row] + str(col)

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

  # Method to take a turn
  def __take_turn(self, turn_count):    # Overwriting to allow AI to decide coordinate and removing super shot
    # Check if the active player's ship list is empty (game over)
    if self.active_player.ship_list == []:
      self.end_game()  # End the game

    # print(f"\n ==== Round #{turn_count} ==== Player {self.active_player.id}'s turn ====\n")  # Print the current turn number and active player
    # print("Your board")  # Print player's own board
    # self.print_board(self.active_player.board)  # Call print_board() to display active player's board
    # print("Opp's board")  # Print opponent's board
    # self.print_board(self.active_player.opps_board)  # Call print_board() to display the opponent's board

    # coord = self.get_input(f"Player {self.active_player.id} -- Attack a coordinate: ")  # Prompt the active player for a coordinate to attack
    # super_shot = False

    # if (coord[-1].lower() == 's'):              # check for super shot flag
    #   coord = coord[:-1]                           # remove the flag from the coord string
    #   if self.active_player.super_shot:           # checks if super shot has already been used by the player
    #     self.active_player.super_shot = False       # sets flag to False to mark that it has now been used
    #     super_shot = True

    # os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal

    # If the input is a valid coordinate
    coord = self.aiTurn() # return value needs to be set accordingly so that it can be passed into here

    if self.valid_coord(coord):
      # Check if the coordinate has already been attacked
      if coord not in self.active_player.attacked_coords:
        self.active_player.attacked_coords.append(coord)  # Add the coordinate to the list of attacked coordinates
        self.active_player.attack_ship(coord)  # Call attack_ship() to attack the ship at the coordinate
        self.turn_count += 1  # Increment the turn count
        self.__switch_turns()  # Switch turns to the other player
      # else:
      #   print("Space already taken. Try again!")  # If the spot has already been attacked, print an error message

    # print("Your board")  # Print player's own board
    # self.print_board(self.active_player.board)  # Call print_board() to display active player's board
    # print("Opp's board")  # Print opponent's board
    # self.print_board(self.active_player.opps_board)  # Call print_board() to display the opponent's board
    # self.br()
    # print("Pass the screen to the next player")

    # time.sleep(8)
    # os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal
    self.__take_turn(self.turn_count) # NEEDS TO CHANGE, CURRENTLY OVERWRITING GAMEOBJECT FUNCTION WHICH CAUSES PROBLEMS # Call __take_turn() recursively to continue the game


  def attack_ship(self, coord):   # Overwriting to not contain super shot logic
    # need a boalean return for this so we can mark the opponents board when a hit(true)
    row, col = self.coord_translator(coord)
    self.hit(row, col) if isinstance(self.opp.board[row][col], Ship) else  self.miss(row, col)


  # End shooting functions =========================================================

  # AI decision functions ==========================================================

  def aiTurn(self):   #Function that will handle all behavior for the ai shooting, returns a valid coordinate to shoot at
    alphaCoords = ['a','b','c','d','e','f','g','h','i','j']   #Helper list of the y coord letters

    if self.aiPrevShot != 'none':                 #Check if the game has started and self.aiPrevShot is not 'none'
      self.aiHitCoords.append(self.aiPrevShot)    #If the game had not just started, add the value of aiPrevShot into list aiHitCoords

#-----------------------------------------------START OF EASY DIFFICULTY ------------------------------------------------------------------------ 
#Get list of spaces that have been hit so far and choose a letter and number combo that has not been hit
    
    if(self.difficulty == 'easy'):  #Check if difficulty has been set to 'easy'
      
      validCoord = False                    #Var to start/stop while loop
      while not validCoord:                 #Start looping
        coord = random.choice(alphaCoords) + str(random.randint(1,10))  #Set letter and number values to random values
        
        if coord not in self.aiHitCoords:   #Check if the randomly selected combo has already been touched by the ai
          validCoord = True                 #If it has not been, break out of the loop
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
    

      if(self.aiPrevShot != 'none' or self._aiHit(self.aiPrevShot) == True): #Check if it is the start of the game or the previous shot was a hit
        if(self.sameShip == False):             #Check if the ai is still trying to sink the same ship as it was last turn
          self.originalHit = self.aiPrevShot    #Set the coordinate of the first contact of the ship if a hit has been landed on a ship for the first time
          self.sameShip = True                  #Set sameShip to true, which will lock in the above coordinate until the ship gets sunk

        validCoord = False                      #Variable to start both loops
        while(not(validCoord)):                 #Loop that will end whenever a valid coordinate is found
          if(not(self.randomMoves)):            #Check if the set of possible random moves is completely empty
            self.aiPrevShot = self.originalHit  #If so, this means the ai cannot make any valid moves and must return to the first coordinate it hit
          
          self.randomMoves = [0,1,2,3]          #Reset the set of random moves every new turn

          while(not(validCoord) and (self.randomMoves)):  #loop until valid coord is found or the ai runs out of moves
            nextShot = random.choose(self.randomMoves)    #chose a random move: 0-right, 1-left, 2-down, 3-up

            #----------------------------------------------RIGHT SELECTION------------------------------------------------------
            if(nextShot == 0):    #Check to the right of the current location
              if(alphaCoords[alphaCoords.index(self.aiPrevShot[0])] != 'j'):  #Make sure the current location isn't the rightmost position
                coord = alphaCoords[(alphaCoords.index(self.aiPrevShot[0])+1)] + self.aiPrevShot[1] #If it isn't, try to hit to the right
              self.randomMoves.remove(0)  #Remove the possibility of going right again
            #----------------------------------------------RIGHT SELECTION------------------------------------------------------

            #----------------------------------------------LEFT SELECTION------------------------------------------------------
            elif(nextShot == 1):  #Check to the left of the current location
              if(alphaCoords[alphaCoords.index(self.aiPrevShot[0])] != 'a'): #Make sure the current location isn't the leftmost position
                coord = alphaCoords[(alphaCoords.index(self.aiPrevShot[0])-1)] + self.aiPrevShot[1] #If it isn't, try to hit to the left
              self.randomMoves.remove(1)  #Remove the possibility of going left again
            #----------------------------------------------LEFT SELECTION------------------------------------------------------

            #----------------------------------------------DOWN SELECTION------------------------------------------------------
            elif(nextShot == 2):  #Check below the current location
              if(int(self.aiPrevShot[1]) < 10): #Make sure the current location isn't the bottommost position
                coord = self.aiPrevShot[0] + str(int(self.aiPrevShot[1]) + 1) #If it isn't, try to hit down
              self.randomMoves.remove(2)  #Remove the possibility of going down again
            #----------------------------------------------DOWN SELECTION------------------------------------------------------

            #----------------------------------------------UP SELECTION------------------------------------------------------
            else:   #Check above the current location
              if(int(self.aiPrevShot[1]) > 1):  #Make sure the current location isn't the topmost position
                coord = self.aiPrevShot[0] + str(int(self.aiPrevShot[1]) - 1) #If it isn't, try to hit up
              self.randomMoves.remove(3)  #Remove the possibility of going up again
            #----------------------------------------------UP SELECTION------------------------------------------------------

            if coord not in self.aiHitCoords: #Once coord has been found, make sure it has not already been hit
                validCoord = True #If this is a valid coordinate, set validCoord to true and break out of both loops
                #self.aiPrevShot = coord
      
      #---------------------------------------------------Random selection------------------------------------------------------
      else: 
        validCoord = False                  #Var to start/stop while loop
        while not validCoord:               #Start Looping
          coord = random.choice(alphaCoords) + str(random.randint(1,10))  #Set letter and number values to random values
          
          if coord not in self.aiHitCoords: #Check if the randomly selected combo has already been touched by the ai
            validCoord = True               #If it has not bee, break out of the loop
        #self.aiPrevShot = coord
      #---------------------------------------------------Random selection------------------------------------------------------
    
#-----------------------------------------------START OF HARD DIFFICULTY------------------------------------------------------------------------ 
#The ai will know the position of all ships and will hit one every turn it takes

    elif(self.difficulty == 'hard'):        #Check if the difficulty has been set to 'hard'
      if(not(self.aiHitCoords)):            #Check if the list of previous locations the ai has touched is empty
        coord = self.tempShipCoordsList[0]  #If so, set the coordinate to the first item in the list of all ship coordinates
      else:                                   
        coord = self.tempShipCoordsList(self.tempShipList.index(self.aiPrevShot) + 1) #If not, find the position of the last shot coord in the ship coordinate list and go to the next index
      
    self.aiPrevShot = coord   #Set the last shot the ai took to the one that it found
    return coord              #Return the coordinate the ai found
  
  def _aiHit(self, coord):
    #This function currently does not work, but it should be able to return true if a ship was hit, and false if it was missed
    row, col = self.coord_translator(coord)
    if isinstance(self.opp.board[row][col], Ship):
      return True
    else:
      return False

  # End AI decision functions ======================================================