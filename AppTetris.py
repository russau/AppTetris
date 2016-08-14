import random
import cgi
import Tetris
import string
import logging
import json
import re
import time
import urllib, hashlib

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch

header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
    <title>Tetris Code Challenge</title>
    <link rel="shortcut icon" href="/favicon.ico" >
    <link href="/static/style2.css" rel="Stylesheet" />
    <script src="/static/jquery-1.2.6.min.js" language="javascript" type="text/javascript" ></script>
    <script src="/static/jquery.timers.js" language="javascript" type="text/javascript" ></script>
    <script src="/static/jquery.timers.js" language="javascript" type="text/javascript" ></script>
    <script src="/static/jquery.hint.js" language="javascript" type="text/javascript" ></script>
    <script type="text/javascript">
    var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
    document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
    try {
    var pageTracker = _gat._getTracker("UA-777142-4");
    pageTracker._trackPageview();
    } catch(err) {}</script>

    <script language="javascript" type="text/javascript">
        var game = null;

        $(document).ready(function(){
            $('input[title!=""]').hint();

            $().ajaxSend(function(r,s){
                $("#contentLoading").css('visibility','');
            });

            $().ajaxStop(function(r,s){
                $("#contentLoading").css('visibility','hidden');
            });

            $('#btnSave').click(function() {
                $.post("/save", {client_url: $('#client_url').val() }, play);
                return false;
            });

            $('#btnTest').click(function(){
                $('#divBoard').stopTime();
                return false;
            });

            attachHistoryClick();
        });

        function attachHistoryClick()
        {
            $('.history').click(function() {
                $.get("/getgame", { key: $(this).attr('key') }, function(result)
                {
                    showGame(eval(result));
                });
                return false;
            });
        }

        function play()
        {
            $.post("/play", playCompleted);
        }

        function playCompleted(result)
        {
            var game = eval('(' + result + ')');

            if (game.inplay)
            {
                $.post("/play", { key: game.key }, playCompleted);
            }
            else
            {
                $("#divHistory").load("/gethistory", attachHistoryClick);
                showGame(game.gameResults);
            }
        }

        function showGame(game)
        {
            if (!game) {
                return;
            }
            $('#divBoard').stopTime();
            $('.row').empty();
            num = 0;

            $('#divBoard').everyTime(200, function()
            {
                var val = game[num];
                copyPieceToFinalPosition(val);
                num++;
            }, game.length);
        }

        function copyPieceToFinalPosition(val)
        {
            var drops = 20 - val.dropY - 1;
            for (var y = 0; y < val.piece.length; y++) {
                for (var x = 0; x < val.piece[y].length; x++) {
                    if (val.piece[y][x]) {
                        var square = $('<img class="sq"/>').attr('src', '/static/' + val.piecech + '.png').css('left', (x + val.dropX) * 24);
                        $('.row:visible').eq(drops + y).append(square);
                    }
                }
            }

            // fade out any rows that need to be deleted
            $.each(val.deleteRows, function(index, val) {
                //$('.row:visible').eq(19 - val).fadeOut(100, function() {
                //    $('#divBoard').prepend($('<div class="row"></div>'));
                //});
                $('.row:visible').eq(19 - val).hide();
                $('#divBoard').prepend($('<div class="row"></div>'));
            });
        }

    </script>

</head>
<body>
"""

footer = """
</body>
</html>
"""

class GameHistory(db.Model):
    owner = db.UserProperty()
    client_url = db.StringProperty()
    exception = db.StringProperty()
    datetime = db.DateTimeProperty(auto_now=True)
    game_data = db.TextProperty()
    score = db.IntegerProperty()
    moves = db.IntegerProperty()
    board_session = db.TextProperty()
    game_complete = db.BooleanProperty()

class Registration(db.Model):
    owner = db.UserProperty()
    client_url = db.StringProperty()
    topscore = db.IntegerProperty()
    topgame = db.ReferenceProperty(GameHistory)


class Root(webapp.RequestHandler):
    def get(self):
        self.response.out.write(header)
        self.response.out.write("""
    <p><img src="/static/logo.png"/></p>
    <p>
        <img src="/static/l.png"/>
        <img src="/static/j.png"/>
        <img src="/static/o.png"/>
        <img src="/static/i.png"/>
        <img src="/static/t.png"/>
        <img src="/static/s.png"/>
        <img src="/static/z.png"/>
    </p>
""")

        user = users.get_current_user()
        self.response.out.write("""<p><a href="/static/howto.html">How to play...</a> """)

        if not user:
            self.response.out.write("<a href=\"%s\">Sign in to compete!</a> <a href=""mailto:tetrischallenge@gmail.com"">tetrischallenge@gmail.com</a></p>" %
            users.create_login_url("/"))

        else:
            self.response.out.write("User: %s (<a href=\"%s\">sign out</a>) <a href=""mailto:tetrischallenge@gmail.com"">tetrischallenge@gmail.com</a></p>" %
            (user.nickname(), users.create_logout_url("/")))

            registrations = db.GqlQuery("SELECT * FROM Registration WHERE owner = :1", users.get_current_user())
            registration  = registrations.get()
            if registration:
                client_url = registration.client_url
            else:
                client_url = ""

            self.response.out.write("""
            <form>
                <p><input type="text" id="client_url" value="%s" title="http://pyclient.appspot.com/" size="40" />
                <button id='btnSave'>Play!</button>
                <img id="contentLoading" src="/static/loading.gif" style="visibility:hidden"/></p>
            </form>
            """ % client_url)


        self.response.out.write("""
            <table border="0">
            <tr><td valign="top">
            <div style="width:240px; height:480px; background-color:Black; padding: 0px; border: solid 1px red; position:relative" id="divBoard">
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            <div class="row"></div>
            </div>
            </td>
            <td valign="top">
                %s
            </td>
            </tr>
            </table>
            """ % buildHistoryTable())

        self.response.out.write(footer)

def buildHistoryTable():
    gamehistories = db.GqlQuery("SELECT * FROM GameHistory WHERE owner = :1 ORDER BY datetime DESC LIMIT 10", users.get_current_user())

    table = ""

    if users.get_current_user():
        table = """<div id="divHistory"><table style="background-color:Black; padding: 0px; border: solid 1px red; font-family: monospace; color: white">"""
        table += """<tr><td>time (utc)</td> <td>score</td> <td>moves</td><tr>"""
        for gameHistory in gamehistories:
            if gameHistory.game_complete is None or gameHistory.game_complete:  # old rows have None as this is a new property
                if gameHistory.exception is not None:
                    table += """<tr><td>%s</td><td colspan="3" class="error">%s</td><tr>""" % (gameHistory.datetime.strftime("%Y-%m-%d %H:%M:%S"), gameHistory.exception)
                else:
                    table += """<tr><td>%s</td> <td>%d</td> <td>%d</td> <td><a href="#" class="history" key="%s">Re-play</a></td><tr>""" % (gameHistory.datetime.strftime("%Y-%m-%d %H:%M:%S"), gameHistory.score, gameHistory.moves, gameHistory.key())

        table += """</table>"""


    topscores = db.GqlQuery("SELECT * FROM Registration ORDER BY topscore DESC LIMIT 10")

    table += """<div id="divHistory"><table style="background-color:Black; padding: 0px; border: solid 1px red; font-family: monospace; color: white">"""
    table += """<tr><td colspan="2" style="font-weight: bold">high scores</td><tr>"""
    table += """<tr><td>user</td> <td>score</td><tr>"""
    for registration in topscores:
        if registration.topscore is not None:

            email = registration.owner.email
            default = "http://tetrisapp.appspot.com/static/j.png"
            size = 24

            # construct the url
            gravatar_url = "http://www.gravatar.com/avatar.php?"
            gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email().lower()).hexdigest(), 'default':default, 'size':str(size)})


            table += """<tr><td><img src="%s" /></td><td>%s</td> <td>%d</td><td>""" % (gravatar_url, registration.owner, registration.topscore)

            if registration.topgame:
                table += """<a href="#" class="history" key="%s">Re-play</a>""" % str(registration.topgame.key())

            table += """</td></tr>"""

    table += """</table></div>"""

    return table


class GetHistoryTable(webapp.RequestHandler):
    def get(self):
        self.response.out.write(buildHistoryTable())

class GetGame(webapp.RequestHandler):
    def get(self):
        key = self.request.get('key')
        history = GameHistory.get(key)
        self.response.out.write(history.game_data)

class Debugging(webapp.RequestHandler):
    def get(self):
        self.response.out.write("<table>")
        scores = db.GqlQuery("SELECT * FROM GameHistory WHERE score in (940, 900, 895, 860, 560) ORDER BY score, datetime ")
        for gameHistory in scores:
            self.response.out.write("<tr><td>%s</td><td>%s</td><td>%d</td><td>%s</td></tr>" % (gameHistory.owner.email(), gameHistory.datetime.strftime("%Y-%m-%d %H:%M:%S"), gameHistory.score, gameHistory.key()) )
            #<td>%s</td><td>%s</td><td>%s</td>
            #

        self.response.out.write("<table>")


class Save(webapp.RequestHandler):
    def post(self):
        registrations = db.GqlQuery("SELECT * FROM Registration WHERE owner = :1", users.get_current_user())
        registration  = registrations.get()
        if not registration:
            registration = Registration()
            registration.owner = users.get_current_user()

        registration.client_url = self.request.get('client_url')
        registration.put()

class Play(webapp.RequestHandler):

    def post(self):
        registrations = db.GqlQuery("SELECT * FROM Registration WHERE owner = :1", users.get_current_user())
        registration  = registrations.get()
        key = self.request.get("key")

        t = Tetris.Tetris();

        inplay = True;
        totalscore = 0
        moves = 0
        batchmoves = 0

        # we've been passed a key, load session from the database
        if key != '':
            gameHistory = GameHistory.get(key)
            t.board = eval(gameHistory.board_session)
            t.gameResults = eval(gameHistory.game_data)
            totalscore = gameHistory.score;
            moves = gameHistory.moves;
        else:
            gameHistory = GameHistory()
            gameHistory.client_url = registration.client_url
            gameHistory.owner = registration.owner

        while (batchmoves < 10 and inplay and moves < 200):
            piece = random.choice(['i','j','l','o','s','t','z'])
            url = registration.client_url
            try:
                result = urlfetch.fetch(url, "piece=%s&board=%s" % (piece, t.boardToPOSTString()), "POST")
            except: #  urlfetch.InvalidURLError() come back to this
                gameHistory.exception = "Bad url"
                gameHistory.put()
                self.response.out.write("[]")
                return
    ##            except:
    ##                gameHistory.exception = "Error"
    ##                gameHistory.put()
    ##                self.response.out.write("[]")
    ##                return


            r = re.compile("position=(\\d+)&degrees=(\\d+)")
            try:
                position = int(r.match(result.content).group(1))
                degrees = int(r.match(result.content).group(2))
            except: #  urlfetch.InvalidURLError() come back to this
                gameHistory.exception = "Error reading client reponse"
                gameHistory.put()
                self.response.out.write("[]")
                return

            inplay, score = t.dropPiece(position, piece, degrees)
            totalscore += score
            moves += 1
            batchmoves += 1


        if inplay and moves < 200:
            gameHistory.board_session = str(t.board)
            gameHistory.game_data = str(t.gameResults)
            gameHistory.moves = moves
            gameHistory.score = totalscore
            gameHistory.put()

            response = {}
            response['inplay'] = inplay
            response['key'] = str(gameHistory.key())

        else:
            jsonResults = json.dumps(t.gameResults)
            gameHistory.game_data = jsonResults
            gameHistory.score = totalscore
            gameHistory.moves = moves
            gameHistory.game_complete = True
            gameHistory.put()

            response = {}
            response['inplay'] = False
            response['gameResults'] = t.gameResults

        if totalscore > registration.topscore:
            registration.topscore = totalscore
            registration.topgame = gameHistory
            registration.put()

        self.response.out.write(json.dumps(response))



class RandomClient(webapp.RequestHandler):
    def get(self):
        self.response.out.write("try POSTing")

    def post(self):
        pos = random.choice(range(10))
        degrees = random.choice([0,90,180,270])

        piece = self.request.get("piece")
        board = self.request.get("board")

        self.response.out.write("position=%d&degrees=%d" % (pos, degrees))

application = webapp.WSGIApplication(
                                     [
                                     ('/', Root)
                                     ,('/save', Save)
                                     ,('/play', Play)
                                     ,('/gethistory', GetHistoryTable)
                                     ,('/getgame', GetGame)
                                     ,('/random_client', RandomClient)
                                     ,('/russ_qwerty', Debugging)
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
