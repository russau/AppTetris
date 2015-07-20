using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Drawing;
using System.Diagnostics;

namespace RrsTetris.Classes
{
    public class Player
    {
        private Dictionary<char, int[,]> _Pieces;
        private const int HEIGHT = 20;
        private const int WIDTH = 10;

        public Player()
        {
            _Pieces = new Dictionary<char, int[,]>();
            _Pieces.Add('i', new int[,] { { 1 }, { 1 }, { 1 }, { 1 } });
            _Pieces.Add('j', new int[,] { { 0, 1 }, { 0, 1 }, { 1, 1 } });
            _Pieces.Add('l', new int[,] { { 1, 0 }, { 1, 0 }, { 1, 1 } });
            _Pieces.Add('o', new int[,] { { 1, 1 }, { 1, 1 } });
            _Pieces.Add('s', new int[,] { { 0, 1, 1 }, { 1, 1, 0 } });
            _Pieces.Add('t', new int[,] { { 1, 1, 1 }, { 0, 1, 0 } });
            _Pieces.Add('z', new int[,] { { 1, 1, 0 }, { 0, 1, 1 } });
        }

        public int[,] BoardFromString(string board)
        {
            string[] boardLines = board.Split(new char[] { ' ' });
            int[,] boardArray = new int[HEIGHT, WIDTH];

            for (int y = 0; y < HEIGHT; y++)
            {
                for (int x = 0; x < WIDTH; x++)
                {
                    if (boardLines[y][x] != '.')
                    {
                        boardArray[HEIGHT - y - 1, x] = 1;
                    }
                }
            }

            return boardArray;
        }

        public Move GetMove(int[,] board, string piece)
        {
            List<Move> allMoves = AllMoves(board, piece);
            if (allMoves.Count > 0)
            {
                return allMoves[0];
            }
            else
            {
                return new Move { Degrees = 0, Position = 0 };
            }
        }

        private List<Move> AllMoves(int[,] board, string piece)
        {
            List<Move> allMoves = new List<Move>();
            // try every rotation / every position across the board
            for (int x = 0; x < WIDTH; x++) 
            {
                for (int i = 0; i < 4; i++)
                {
                    int[,] piecearr = RotatePiece(_Pieces[piece[0]], i);
                    int pieceWidth = piecearr.GetUpperBound(1) + 1;
                    int pieceHeight = piecearr.GetUpperBound(0) + 1;

                    // make sure this orientation fits in the board
                    if (x <= WIDTH - pieceWidth)
                    {
                        int y = GetFallPosition(board, piecearr, x);
                        
                        if (y > HEIGHT - 1) // dropping it here would go off the board
                        {
                            break;
                        }
                        List<Point> adjacent = GetAdjacentPositions(piecearr, new Point(x, y));

                        // work out if that just wiped out any lines
                        int[,] newboard = new int[HEIGHT, WIDTH];
                        Array.Copy(board, newboard, board.Length);
                        // copy the rotate piece in the new board
                        for (int piecey = 0; piecey < pieceHeight; piecey++)
                        {
                            for (int piecex = 0; piecex < pieceWidth; piecex++)
                            {
                                if (piecearr[piecey, piecex] == 1)
                                {
                                    newboard[y - piecey, x + piecex] = 1;
                                }
                            }
                        }

                        int weighting = 0;
                        for (int boardy = 0; boardy < HEIGHT; boardy++)
                        {
                            bool lineout = true;
                            for (int boardx = 0; boardx < WIDTH; boardx++)
                            {
                                if (newboard[boardy, boardx] != 1)
                                {
                                    lineout = false;
                                    break;
                                }
                            }

                            if (lineout)
                            {
                                weighting += 1000;
                            }
                        }                        

                        BoardArrayDebug(newboard);
                        // spin thru the adjacent positions 
                        foreach (Point p in adjacent)
                        {
                            // adjacent to a screen edge
                            if (p.Y < 0)
                            {
                                weighting += 11;
                            }
                            else if (p.X < 0 || p.X > WIDTH - 1)
                            {
                                weighting += 10;
                            }
                            else if (p.Y > HEIGHT - 1)
                            {
                                weighting += 0;
                            }
                            //  adjacent to another piece
                            else if (board[p.Y, p.X] == 1)
                            {
                                weighting += 10;
                            }
                        }
                        allMoves.Add(new Move { Position = x, Degrees = i * 90, Weighting=weighting });
                    }
                }
            }

            allMoves.Sort(delegate(Move move1, Move move2)
            {
                return move2.Weighting.CompareTo(move1.Weighting);
            });
            return allMoves;
        }

        private void BoardArrayDebug(int[,] board)
        {
            Debug.WriteLine("---------------------");
            for (int y = HEIGHT - 1; y >= 0; y--)
            {
                for (int x = 0; x < WIDTH; x++)
                {
                    Debug.Write(board[y, x].ToString());
                }
                Debug.WriteLine("");
            }
        }

        private int[,] RotatePiece(int[,] piece, int times)
        {
            int[,] copyOf = new int[piece.GetUpperBound(0) + 1, piece.GetUpperBound(1) + 1];
            Array.Copy(piece, copyOf, piece.Length);
            if (times == 0)
                return copyOf;

            int[,] piecen = null;
            for (int i = 0; i < times; i++)
            {
                piecen = new int[copyOf.GetUpperBound(1) + 1, copyOf.GetUpperBound(0) + 1];
                for (int y = 0; y <= copyOf.GetUpperBound(0); y++)
                {
                    for (int x = 0; x <= copyOf.GetUpperBound(1); x++)
                    {
                        piecen[x, copyOf.GetUpperBound(0) - y] = copyOf[y, x];
                    }
                }

                copyOf = new int[copyOf.GetUpperBound(1) + 1, copyOf.GetUpperBound(0) + 1];
                Array.Copy(piecen, copyOf, piecen.Length);
            }

            return piecen;
        }


        /// <summary>
        /// where will this piece stop
        /// </summary>
        private int GetFallPosition(int[,] board, int[,] piece, int xPosition)
        {
            int width = piece.GetUpperBound(1) + 1;
            int height = piece.GetUpperBound(0) + 1;
            int[] boardHeights = new int[width];
            int[] pieceHeights = new int[width];

            for (int y = 0; y < HEIGHT; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    if (board[y, x + xPosition] == 1) boardHeights[x] = y + 1;
                }
            }

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    if (piece[y, x] == 1) pieceHeights[x] = y + 1;
                }
            }

            int max = 0;
            for (int i = 0; i < width; i++)
            {
                int sum = boardHeights[i] + pieceHeights[i];
                if (sum > max) max = sum;
            }
            return max-1;
        }

        /// <summary>
        /// return all the coordinates around a piece
        /// </summary>
        private List<Point> GetAdjacentPositions(int[,] piece, Point position)
        {
            List<Point> points = new List<Point>();
            List<Point> piecePoints = new List<Point>();
            for (int y = 0; y <= piece.GetUpperBound(0); y++)
            {
                for (int x = 0; x <= piece.GetUpperBound(1); x++)
                {
                    if (piece[y, x] == 1)
                    {
                        Point north = new Point(position.X + x, position.Y - y + 1);
                        Point east = new Point(position.X + x + 1, position.Y - y);
                        Point south = new Point(position.X + x, position.Y - y - 1);
                        Point west = new Point(position.X + x - 1, position.Y - y);

                        List<Point> newPoints = new List<Point>(new Point[] { north, east, south, west });

                        piecePoints.Add(new Point(position.X + x, position.Y - y));

                        foreach (Point point in newPoints)
                        {
                            bool inPiece = false;
                            int offsetX = point.X - position.X;
                            int offsetY = position.Y - point.Y;
                            if (offsetX >= 0 && offsetX <= piece.GetUpperBound(1)
                                && offsetY >= 0 && offsetY <= piece.GetUpperBound(0))
                            {
                                inPiece = piece[offsetY, offsetX] == 1;
                            }

                            if (!points.Contains(point) && !inPiece) //  
                            {
                                points.Add(point);
                            }
                        };
                    }
                }
            }
            return points;
        }
    }



    public class Move
    {
        public int Degrees { get; set; }
        public int Position { get; set; }
        public int Weighting { get; set; }
    }
}
