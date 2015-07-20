using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using RrsTetris.Classes;

namespace TinIsles.RrsTetris
{
    public class Handler : IHttpHandler
    {

        public void ProcessRequest(HttpContext context)
        {
            string board = context.Request.Form["board"];//".......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... zzzzzzzz..";
            string piece = context.Request["piece"]; //"l";  

            Player p = new Player();
            int[,] boardArray = p.BoardFromString(board);
            Move m = p.GetMove(boardArray, piece);
            
            context.Response.Write(string.Format("position={0}&degrees={1}", m.Position, m.Degrees));

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
