#!/usr/bin/env python

from copy import copy
import random
import re
import json


BOARD_HEIGHT = 20
BOARD_WIDTH = 10

def main():
    t = Tetris();
    inplay = True;
    score = 0
    totalscore = 0



    #while inplay:
    piece = random.choice(['i','j','l','o','s','t','z'])
    pos = random.choice(range(10))
    degrees = random.choice([0,90,180,270])
    #inplay, score = t.dropPiece(pos,piece,degrees)




    inplay, score = t.dropPiece(5,'l',90)
    inplay, score = t.dropPiece(1,'o',0)
    inplay, score = t.dropPiece(0,'t',0)
    inplay, score = t.dropPiece(1,'i',0)
    inplay, score = t.dropPiece(8,'l',180)
    inplay, score = t.dropPiece(0,'j',270)
    inplay, score = t.dropPiece(3,'o',0)
    inplay, score = t.dropPiece(0,'z',0)
    inplay, score = t.dropPiece(6,'i',90)
    inplay, score = t.dropPiece(7,'z',0)
    inplay, score = t.dropPiece(0,'o',0)
    inplay, score = t.dropPiece(7,'t',180)
    inplay, score = t.dropPiece(7,'t',180)
    inplay, score = t.dropPiece(3,'s',90)
    inplay, score = t.dropPiece(4,'s',0)
    inplay, score = t.dropPiece(0,'s',90)
    inplay, score = t.dropPiece(2,'t',270)
    inplay, score = t.dropPiece(3,'j',90)
    inplay, score = t.dropPiece(7,'l',0)
    inplay, score = t.dropPiece(7,'z',0)
    inplay, score = t.dropPiece(6,'j',180)
    inplay, score = t.dropPiece(7,'z',0)
    inplay, score = t.dropPiece(2,'o',0)
    inplay, score = t.dropPiece(7,'l',90)
    inplay, score = t.dropPiece(3,'l',270)
    inplay, score = t.dropPiece(7,'z',0)


    totalscore += score
    print "======================"

    t.printBoard()
    print json.write(t.gameResults)

    print "totalscore: ", totalscore


class Tetris:

    def __init__(self):
        self.board = [['.','.','.','.','.','.','.','.','.','.'] for x in range(BOARD_HEIGHT)]
        self.gameResults = []
    
    def setBoard(self, newBoard):
        board = copy(newBoard)

    def dropPiece(self, pos, piecech, degrees):
        g = {};
        g['piecech'] = piecech
        g['deleteRows'] = []

        if piecech == 'i':
            piece = [[1],[1],[1],[1]]
        elif piecech == 'j':
            piece = [[0,1],[0,1],[1,1]]
        elif piecech == 'l':
            piece = [[1,0],[1,0],[1,1]]
        elif piecech == 'o':
            piece = [[1,1],[1,1]]
        elif piecech == 's':
            piece = [[0,1,1],[1,1,0]]
        elif piecech == 't':
            piece = [[1,1,1],[0,1,0]]
        elif piecech == 'z':
            piece = [[1,1,0],[0,1,1]]
            
        rotated = self.rotatePiece(piece, degrees)
        g['piece'] = rotated

        
        height = len(rotated)
        width = len(rotated[0])
        maxpos = BOARD_WIDTH - width         #what's the furthest along this piece could go
        pos = min([pos, maxpos])    # bring in a piece that's too far right
        
        boardheight = [0  for i in range(width)]
        for x in range(width):
            for y in range(BOARD_HEIGHT):
                if self.board[y][pos + x] != '.':
                    boardheight[x] = y+1
                    
        
        pieceheight = [0 for i in range(width)]
        
        for x in range(width):
            for y in range(height):
                if rotated[y][x] == 1:
                    pieceheight[x] = y+1

        sum = [boardheight[i]+pieceheight[i] for i in range(width)]
        if max(sum) > BOARD_HEIGHT:
            return False, 0

        destx, desty = pos, max(sum)-1
        g['dropY'] = desty;
        g['dropX'] = destx

        # copy the rotated piece to its dest on the board
        for y in range(len(rotated)):
            for x in range(len(rotated[y])):
                if rotated[y][x]==1:
                    self.board[desty-y][destx+x] = piecech
                    
        # test for rows to remove - could be a bit more efficient: break out when u hit a blank row
        row = BOARD_HEIGHT - 1
        rowsremoved = 0
        scores = [0, 10, 25, 40, 55]
        while (row >= 0 ):
            allfull = True
            for x in self.board[row]:
                if (x == '.'):
                    allfull = False
                    break
            if allfull:
                del self.board[row]
                g['deleteRows'].append(row)
                self.board.append(['.','.','.','.','.','.','.','.','.','.'])
                rowsremoved += 1
            else:
                row -= 1

        self.gameResults.append(g)

        return True, scores[rowsremoved]

    def rotatePiece(self, piece, degrees):
        if degrees == 0:
            piecen = copy(piece)

        for i in range(degrees / 90): #
            piecen = []
            # initialize piecen list to be the rotation of piece
            for y in range(len(piece[0])):
                piecen.append([0 for x in range(len(piece))])

            for y in range(len(piece)):
                for x in range(len(piece[y])):
                        piecen[x][len(piece)-1-y] = piece[y][x]

            piece = copy(piecen)


        return piecen

    def boardToString(self):
        str = ""
        for y in range(len(self.board)-1, -1, -1):
            for x in range(len(self.board[y])):
                str += self.board[y][x]
        return str


    def boardToPOSTString(self):
        str = ""
        rows =  ["".join(self.board[y]) for y in range(len(self.board)-1, -1, -1)]
        return " ".join(rows)

    def printBoard(self):
        #print range(len(self.board)-1, -1, -1)
        for y in range(len(self.board)-1, -1, -1):
            for x in range(len(self.board[y])):
                print self.board[y][x],
            print ""

if __name__ == '__main__':
    main()
