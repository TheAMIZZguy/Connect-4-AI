# Has the properties of a state for the game
class State():
    def __init__(self, playHistory, board, player):
        self.playHistory = list(filter(len, playHistory))
        self.board = board
        self.vicBoard = self.BoardForVictor(board)
        self.player = player

    def IsPlayer(self, player):
        return player == self.player
    
    def Hash(self):
        return str(self.playHistory)
    
    def Hash2(self):
        return str(self.playHistory[:-1])
    
    # Just to visualize the board, removes the 3's from the board to make it easier to read
    def BoardForVictor(self, board):

        protoBoard = [row[:] for row in board]
        
        for row in range(len(protoBoard)):
            for value in range(len(protoBoard[row])):
                if protoBoard[row][value] == 3:
                    protoBoard[row][value] = 0
                    
        return protoBoard
