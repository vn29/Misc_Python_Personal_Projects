#tictactoe game to demonstrate players as class states playing each turn
class Board():
    arr = [[0]*3 for e in range(3)]
    state = None
    played_spots=[]

    def __init__(self):
        self.state = Player1()
    
    def nextTurn(self):
        self.state.nextTurn(self)

    def playPiece(self,coord):
        if coord in self.played_spots:
            print('spot not available')
        elif (-1<coord[0]<3)!=True:
            print('spot not available')
        elif (-1<coord[1]<3)!=True:
            print('spot not available')
        else:
            self.played_spots.append(coord)
            if isinstance(self.state,Player1):
                self.arr[coord[0]][coord[1]] = 'X'
            
            if isinstance(self.state,Player2):
                self.arr[coord[0]][coord[1]] = 'O'

            self.nextTurn()
            print(self.arr)
    


class Player1():
    def nextTurn(self,Board):
        Board.state = Player2()

class Player2():
    def nextTurn(self,Board):
        Board.state = Player1()


if __name__=='__main__':
    board =Board()

    board.playPiece([1,2])
    board.playPiece([1,1])
