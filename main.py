import os
import requests
import json
import sys
cwd = os.getcwd()

game_list=None
json_raw=""
def download_file():
    global game_list
    print("Downloading Game List")
    file_url = 'https://raw.githubusercontent.com/Joshi234/game-backer/master/game_list.json'

    game_list_raw = requests.get(file_url)
    game_list_raw=game_list_raw.content.decode()


    game_list=json.loads(game_list_raw)


    print("Finished!")
def save_game_list():
    print("Saving...")
    json_raw=json.dumps(game_list)


    open(cwd+'/game_list.json',"w+").write(json_raw)
def first_run():
    try:
        open(cwd+'/game_list.json',"r").read()
    except:
        print("This is your first run so we automatically download the current game list and save it to your disk, you update the list by running 'update'")
        download_file()
        save_game_list()
def add_game(name,dir):
    game_list[name]=dir
    save_game_list()
    print("Succesfully added "+name)
def load_game_list():
    global game_list
    game_list_raw=open(cwd+'/game_list.json',"r").read()
    game_list=json.loads(game_list_raw)
def load():
    first_run()
    load_game_list()
load()
while True:
    a=str(input(">>> "))
    if(a=="update"):
        download_file()
        save_game_list()
    elif(a=="help"):
        print('''help: shows this message
update: updates the game list
add: adds a game to the game list. If you want to contribute send your game_list.json to Joshi234#9828 or do a pull request on github
quit/exit: Closes program
''')
    elif(a=="add"):
        add_game(str(input("Game Name: ")),str(input("Dir: ")))
    elif(a=="debug"):
        print(game_list)
    elif(a=="quit"):
        sys.exit()
    elif(a=="exit"):
        sys.exit()