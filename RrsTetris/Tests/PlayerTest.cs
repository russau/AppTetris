using RrsTetris.Classes;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.Drawing;
using System.Collections.Generic;
using System.Diagnostics;
using System;
using System.Linq;

namespace Tests
{
    
    
    /// <summary>
    ///This is a test class for PlayerTest and is intended
    ///to contain all PlayerTest Unit Tests
    ///</summary>
    [TestClass()]
    public class PlayerTest
    {
        string _PrintingBoard = @"..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........
..........";

        int[,] _TestBoard = { { 1, 1, 1, 1, 1, 1, 1, 1, 0, 0 }
                               , { 0, 1, 1, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                               , { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
                           };

        #region test context
        private TestContext testContextInstance;

        /// <summary>
        ///Gets or sets the test context which provides
        ///information about and functionality for the current test run.
        ///</summary>
        public TestContext TestContext
        {
            get
            {
                return testContextInstance;
            }
            set
            {
                testContextInstance = value;
            }
        }
        #endregion

        [TestMethod()]
        [DeploymentItem("TinIsles.RrsTetris.Classes.dll")]
        public void SimulateGame()
        {

        }

        /// <summary>
        ///A test for GetAdjacentPositions
        ///</summary>
        [TestMethod()]
        [DeploymentItem("TinIsles.RrsTetris.Classes.dll")]
        public void GetAdjacentPositionsTest()
        {
            Player_Accessor target = new Player_Accessor(); // TODO: Initialize to an appropriate value
            int[,] piece = target._Pieces['j'];
            List<Point> points = target.GetAdjacentPositions(piece, new Point(5, 5));
            PrintPoints(points);
        }

        private void PrintPoints(List<Point> points)
        {
            string[] boardArray = _PrintingBoard.Split(new string[] { Environment.NewLine }, StringSplitOptions.None);
            foreach (Point point in points)
            {
                if (point.Y >= 0 && point.Y < 20 && point.X >= 0 && point.X < 20)
                {
                    char[] chars = boardArray[19 - point.Y].ToCharArray();
                    chars[point.X] = '*';
                    boardArray[19 - point.Y] = new String(chars);
                }
            }
            Debug.WriteLine(string.Join(Environment.NewLine, boardArray));
        }


        /// <summary>
        ///A test for GetFallPosition
        ///</summary>
        [TestMethod()]
        [DeploymentItem("TinIsles.RrsTetris.Classes.dll")]
        public void GetFallPositionTest()
        {
            Player_Accessor target = new Player_Accessor();

            int[,] piece = target._Pieces['s'];
            piece = target.RotatePiece(piece, 1);
            int actual;
            actual = target.GetFallPosition(_TestBoard, piece, 0);
            Assert.AreEqual(4, actual);
        }

        /// <summary>
        ///A test for AllMoves
        ///</summary>
        [TestMethod()]
        [DeploymentItem("TinIsles.RrsTetris.Classes.dll")]
        public void AllMovesTest()
        {
            Player_Accessor target = new Player_Accessor(); // TODO: Initialize to an appropriate value
            List<Move> moves = target.AllMoves(_TestBoard, "j");
 

            Move m = moves[0];
        }

        /// <summary>
        ///A test for BoardFromString
        ///</summary>
        [TestMethod()]
        public void BoardFromStringTest()
        {
            Player_Accessor target = new Player_Accessor(); // TODO: Initialize to an appropriate value
            string board = ".......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... .......... zzzzzzzz..";
            int[,] actual;
            actual = target.BoardFromString(board);
            target.BoardArrayDebug(actual);
        }
    }
}
