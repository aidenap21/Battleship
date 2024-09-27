import random
from game_object import GameObject
from ship import Ship

class AI(GameObject):
  def __init__(self, difficulty):  # Constructor for GameObject class
    self.difficulty = difficulty  #This is changed to 'easy', 'medium', or 'hard' during game setup
    
    self.aiPrevShot = 'none'  #This is only changed within aiTurn and will hold the last shot the ai made
    self.aiHitCoords = []     #This is only changed within aiTurn and will contain all shots the ai has made
    self.originalHit = ''     #Set whenever ai hits a ship for the first time
    self.sameShip = False     #Lock originalHit until a ship is sunk
    self.randomMoves = []     #List that contains the possibile random moves. Each move gets removed after test

    self.tempShipList = [] # Uhhh temporary lil variable that will need to be the list of all coordinates of enemy ships
    

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
    
      if(self.aiPrevShot != 'none' or self._aiHit(self.aiPrevShot) == True): 
        if(self.sameShip == False):
          self.originalHit = self.aiPrevShot
          self.sameShip = True 

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

