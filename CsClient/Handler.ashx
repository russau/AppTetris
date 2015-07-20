<%@ WebHandler Language="C#" Class="CsClient.Handler" %>
using System;
using System.Collections.Generic;
using System.Web;
using System.Diagnostics;

namespace CsClient
{
    /// <summary>
    /// Summary description for $codebehindclassname$
    /// </summary>
    public class Handler : IHttpHandler
    {
        const int BOARD_WIDTH = 10;

        public void ProcessRequest(HttpContext context)
        {
            Dictionary<char, int[,]> pieces = new Dictionary<char, int[,]>();
            pieces.Add('i', new int[,] { { 1 }, { 1 }, { 1 }, { 1 } });
            pieces.Add('j', new int[,] { { 0,1 }, { 0,1 }, { 1,1 } });
            pieces.Add('l', new int[,] { { 1, 0 }, { 1, 0 }, { 1, 1 } });
            pieces.Add('o', new int[,] { { 1, 1 }, { 1, 1 } });
            pieces.Add('s', new int[,] { { 0, 1, 1 }, { 1, 1, 0 } });
            pieces.Add('t', new int[,] { { 1, 1, 1 }, { 0, 1, 0 } });
            pieces.Add('z', new int[,] { { 1, 1, 0 }, { 0, 1, 1 } });


            string board = context.Request.Form["board"];//".......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... zzzzzzzz..";
            string piece = context.Request["piece"]; //"l";  
            int[,] pieceArray = pieces[piece[0]];


            Random r = new Random();
            int[] degreesOptions = { 0, 90, 180, 270 };
            int rand = r.Next(3);
            int degrees = degreesOptions[rand];
            
            //rotate the piece a random number of times
            for (int i = 0; i < rand; i++)
            {
                pieceArray = TransposeArray(pieceArray);
            }

            int width = pieceArray.GetUpperBound(1) + 1;
            int position = FindLowestStackX(board.Split(new char[] { ' ' }), width);

            Debug.WriteLine("Board: " + Environment.NewLine + board.Replace(" ", Environment.NewLine));
            Debug.WriteLine("Piece: " + piece);
            Debug.WriteLine("Degrees: " + degrees);
            Debug.WriteLine("Width: " + width);
            Debug.WriteLine("Position: " + position);
            Debug.WriteLine("--------------------------------------" );
            

            context.Response.ContentType = "text/plain";
            context.Response.Write(string.Format("position={0}&degrees={1}", position, degrees));
        }

        
        /// <summary>
        /// rotate the piece array around
        /// </summary>
        private int[,] TransposeArray(int[,] x)
        {
            int[,] result = new int[x.GetUpperBound(1)+1, x.GetUpperBound(0)+1];
            int i, j;

            for (i = 0; i <= x.GetUpperBound(0); i++)
                for (j = 0; j <= x.GetUpperBound(1); j++)
                {
                    result[j, i] = x[i, j];
                }

            return result;
        }
        
        /// <summary>
        /// find x coordinate of the lowest group of spaces on the board
        /// </summary>
        private int FindLowestStackX(string[] board, int width)
        {
            int[] heights = new int[BOARD_WIDTH];
            int pos = 0;
            int lowest = Int32.MaxValue;
            
            Array.Reverse(board);
            for (int i = 0; i < board.Length; i++)
            {
                for (int j = 0; j < BOARD_WIDTH; j++)
                {
                    if (board[i][j] != '.') heights[j] = i+1; 
                }
            }
            
            // find the group of 'width' spaces with the lowest max height
            for (int x = 0; x <= BOARD_WIDTH - width; x++)
            {
                int heighest = 0;
                for (int j = 0; j < width; j++)
                {
                    if (heights[x + j] > heighest) heighest = heights[x + j];
                }
                if (heighest < lowest)
                {
                    lowest = heighest;
                    pos = x;
                }
            }
            
            return pos;
        }
    
            
        

        public bool IsReusable
        {
            get
            {
                return false;
            }
        }
    }
}




