import random
import cgi
import logging
import copy

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

BOARD_WIDTH = 10


class PyClient(webapp.RequestHandler):

    def get(self):
        self.response.out.write("try POSTing")

    def post(self):
        degrees = random.choice([0,90,180,270])
        piecech = self.request.get("piece")
        board = self.request.get("board")

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
        position = self.findLowestStackX(board.split(" "), len(piece[0]))

        self.response.out.write("position=%d&degrees=%d" % (position, degrees))
        
    def findLowestStackX(self, boardlist, width):
        """find the group of 'width' spaces with the lowest max height"""
        heights = [0 for  i in range(BOARD_WIDTH) ]
        boardlist.reverse()

        # create a list of the max 'height' of every column
        for i in range(len(boardlist)):
            row = boardlist[i]
            for j in range(BOARD_WIDTH):
                if row[j] != '.':
                    heights[j] = i+1

        # find the group of 'width' spaces with the lowest max height
        lowest = 100
        pos = 0
        for i in range(BOARD_WIDTH-width+1):
            block = heights[i:i+width]
            if max(block) < lowest:
                lowest = max(block)
                pos = i

        return pos
    
    
    def rotatePiece(self, piece, degrees):
        """returns a list of the rotated piece"""
        if degrees == 0:
            piecen = copy.copy(piece)

        for i in range(degrees / 90): #
            piecen = []
            # initialize piecen list to be the rotation of piece
            for y in range(len(piece[0])):
                piecen.append([0 for x in range(len(piece))])

            for y in range(len(piece)):
                for x in range(len(piece[y])):
                        piecen[x][len(piece)-1-y] = piece[y][x]

            piece = copy.copy(piecen)


        return piecen

application = webapp.WSGIApplication(
                                     [
                                     ('/', PyClient)
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
