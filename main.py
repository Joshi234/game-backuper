import os
import requests
import json
import sys
import shutil
cwd = os.getcwd()

game_list={}
json_raw=""
from os.path import expanduser
home = expanduser("~")
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
    try:
        global game_list
        game_list_raw=open(cwd+'/game_list.json',"r").read()
        game_list=json.loads(game_list_raw)
    except:
        print("Error while reading local json file")
def load():

        first_run()
        load_game_list()
    
def backup(dir):
    a=0
    for i in game_list:
        try:
            
            if(game_list[i][0]=="~"):
                
                shutil.copytree(home+game_list[i][1:],dir+r"\\"+i)
                
            else:
                shutil.copytree(game_list[i],dir+r"\\"+i)
            print("Finished copying game save "+i)
            a=a+1

        except:
            e=0
    if(a==0):
        print("Invalid File Location or no game installed that is currently supported")
    else:
        print("Succesfully copied "+str(a)+" games")
load()
def restore(game_name,backup_dir):
        try:
            game_list[game_name]
            if(game_list[game_name][0]=="~"):
                try:
                
                    shutil.rmtree(home+game_list[game_name][1:])
                except:
                    p=0

                try:
                    shutil.copytree(backup_dir+r"/"+game_name,home+game_list[game_name][1:])
                except:
                    print("Can't find the backup path")
            else:
                         
                try:
                    shutil.rmtree(home+game_list[game_name])
                except:
                    p=0
                try:
                    shutil.copytree(backup_dir+r"/"+game_name,game_list[game_name])
                except:
                    print("Can't find the backup path")
            print("Succesfully recovered game "+game_name)
        except:
            print("Could not find your game "+game_name)
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
backup: Backes up every program
restore: restores game
restore_everything: restores every game in a backup dir
''')
    elif(a=="add"):
        add_game(str(input("Game Name: ")),str(input("Dir: ")))
    elif(a=="debug"):
        print(game_list)
    elif(a=="quit"):
        sys.exit()
    elif(a=="exit"):
        sys.exit()
    elif(a=="backup"):
        backup_dir=str(input("Please enter a dir where you want to backup your saves to: "))
        backup(backup_dir)
    elif(a=="restore"):
        restore(str(input("Game Name: ")),str(input("Backup dir: ")))
        
    elif(a=="restore_everything"):
        backup_dir=str(input("Backup dir: "))
        for i in game_list:
            if(os.path.isdir(backup_dir+r'/'+i)):
                str(input("Are you sure you want to recover?: "+i))
                restore(i,backup_dir)