import json

class game:
    piece = [".j", ".j", "jj"]
    dropTo= 2,
    left= 5,
    deleteRows = [1,2,3]


def main():
    #g = json.read('{ "piece": [".j", ".j", "jj"], "dropTo": 2, "left": 5, "deleteRows": [] }') #game();
    
    g = {}; #{"piece": [], "dropTo": -1, "left": -1, "deleteRows": []}
    g['piece'] =[".j", ".j", "jj"]
    g['dropTo'] = 2;
    g['left'] = 5
    g['deleteRows'] = [1,2,3]
    
    game = []
    game.append(g)
    
    print json.write(game);
    

if __name__ == "__main__":
  main()