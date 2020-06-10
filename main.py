import os
import requests
import json
import sys
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
cwd = os.getcwd()
font=("Arial",20)
font_smaller=("Arial",13)
game_list={}
json_raw=""
from os.path import expanduser
home = expanduser("~")
version="1.2"
config={"standardDir":None,"version":version,"steamId":None,"steamDir":r"C:\Program Files (x86)\Steam\userdata"}
defaultConfig={"standardDir":None,"version":version,"steamId":None,"steamDir":r"C:\Program Files (x86)\Steam\userdata"}

def getSteamUserId():

    config['steamId']=os.listdir(r"C:\Program Files (x86)\Steam\userdata")[0]
    saveConfig()

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
def remove_game(game_name):
    for i in game_list:
        if(i==game_name):
            del game_list[i]
            save_game_list()
            return True
    return False
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
    return True
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
def setConfig(name,value):
    return None
def saveConfig():
    json_raw=json.dumps(config)
    open(cwd+'/config.json',"w+").write(json_raw)
def loadConfig():
    global config
    config=json.loads(open(cwd+"/config.json","r+").read())
def backup(dir):
    a=0
    for i in game_list:
        try:
            
            if(game_list[i][0]=="~"):
                
                shutil.copytree(home+game_list[i][1:],dir+r"\\"+i)
            elif(game_list[i][0]=="+"):
                
                shutil.copytree(config["steamDir"]+r"/"+config["steamId"]+r"/"+game_list[i][1:],dir+r"\\"+i)
                
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
    return a

def restore(game_name,backup_dir):
        try:
          
            game_list[game_name]
            if(game_list[game_name][0]=="~"):
                if(os.path.isdir(backup_dir+r"/"+game_name)):
                    try:
                    
                        shutil.rmtree(home+game_list[game_name][1:])
                    except:
                        p=0

                    try:
                        shutil.copytree(backup_dir+r"/"+game_name,home+game_list[game_name][1:])
                        print("Succesfully recovered game "+game_name)
                        return True
                    except:
                        print("Can't find the backup path")
            elif(game_list[game_name][0]=="+"):
                if(os.path.isdir(backup_dir+r"/"+game_name)):
                    try:
                        shutil.rmtree(config["steamDir"]+r"/"+config["steamId"]+r"/"+game_list[game_name][1:])
                    except:
                        p=0
                    try:
                        shutil.copytree(backup_dir+r"/"+game_name,config["steamDir"]+r"/"+config["steamId"]+r"/"+game_list[game_name][1:])
                        return True
                    except:
                        print("There was an error while copieng save")
                else:
                    print("Cant find backup folder or backup")
                
            else:
                if(os.path.isdir(backup_dir+r"/"+game_name)):
                    try:
                        shutil.rmtree(home+game_list[game_name])
                    except:
                        p=0
                    try:
                        shutil.copytree(backup_dir+r"/"+game_name,game_list[game_name])
                        print("Succesfully recovered game "+game_name)
                        return True
                    except:
                        print("Can't find the backup path")
                else:
                    print("Cant find backup folder or backup")
            
        except:
            print("Could not find your game "+game_name)
def resetConfig():
    config=defaultConfig
    saveConfig()
def add_steam_game(name,appId):
    game_list[name]="+"+appId
    save_game_list()
class Application(tk.Frame):
    
    def first_run_wi(self):
        try:
            loadConfig()
        except:
            print("Creating config")
            config=defaultConfig
            try:
                getSteamUserId()
            except:
                print("Couldn't find Steam User id")
            saveConfig()
            loadConfig()
        try:
            open(cwd+'/game_list.json',"r").read()
        except:
            messagebox.showinfo("Info","Since this is the first time you are running this program we automatically download the newest game list. Later on you can update it with 'update game list'")
            download_file()
            save_game_list()
    def __init__(self, master=None):
        self.first_run_wi()
        load()
        super().__init__(master)
       
        self.master = master
        self.master.title("Game Backer")
        self.master.minsize(300,150)
        self.pack()
        self.create_widgets()
        
    def update_game_list_window(self):
        download_file()
        save_game_list()
        messagebox.showinfo("Succes!","Succesfully updated the game list")
    def options_save(self):
        config["steamDir"]=self.steamDir.get()
        
        saveConfig()
        messagebox.showinfo("Succes!","Succesfully saved config")
    def options_window(self):

        self.top=tk.Toplevel()
        self.user_input=tk.StringVar(self.top)
        self.top.title("Options")
        
        self.select_folder = tk.Button(self.top, text="Reset Steam Id",command=getSteamUserId ,width=25,font=font_smaller)
        self.select_folder.pack()
        self.steamDir=tk.StringVar(self.top)
        self.steamDir.set(config["steamDir"])
        self.top_text_steam=tk.Entry(master=self.top,font=font_smaller,textvariable=self.steamDir,width=25)
        self.top_text_steam.pack()
        self.select_folder = tk.Button(self.top, text="Reset config",command=resetConfig,width=25,font=font_smaller)
        self.select_folder.pack()

        self.save= tk.Button(self.top, text="Save",command=self.options_save,width=25,font=font_smaller)
        self.save.pack()
#steamDir
        self.top_button_dismiss=tk.Button(self.top,text="Dismiss",command=self.top.destroy,font=font_smaller,width=25, fg="red")
        self.top_button_dismiss.pack()
    def add_game_window(self):
        self.title="Select game save folder"
        self.top=tk.Toplevel()
        self.user_input=tk.StringVar(self.top)
        self.top.title("Add Game")
        self.top_label=tk.Label(text="Game name:",master=self.top,font=font_smaller)
        self.top_label.pack()
        self.top_text=tk.Entry(master=self.top,font=font_smaller,textvariable=self.user_input,width=25)
        self.top_text.pack()
        self.filename=tk.StringVar(self.top)
        self.top_text=tk.Entry(master=self.top,font=font_smaller,textvariable=self.filename,width=25)
        self.top_text.pack()
        self.isRelativeDir=tk.BooleanVar(master=self.top)
        self.isRelative=tk.Checkbutton(self.top,text="Is relative (uses home folder)",variable=self.isRelativeDir,font=font_smaller)
        self.isRelative.pack()
        self.isSteamVar=tk.BooleanVar(master=self.top)
        self.isSteam=tk.Checkbutton(self.top,text="Is in steam userdata folder (just enter the appid in save",variable=self.isSteamVar,font=font_smaller)
        self.isSteam.pack()
        self.add = tk.Button(self.top, text="Add Game", command=self.verify_answer_add ,width=25,font=font_smaller)
        self.add.pack()
        self.top_button_dismiss=tk.Button(self.top,text="Dismiss",command=self.top.destroy,font=font_smaller,width=25, fg="red")
        self.top_button_dismiss.pack()
    def get_folder(self):
        self.filename=filedialog.askdirectory(title=self.title)
    def verify_answer_add(self):

        if (self.user_input.get()==""):
            messagebox.showerror("Error","You haven't entered a game name")
        elif(self.filename==None):
            messagebox.showerror("Error","You haven't selected a save folder")
        else:

            if(self.isRelativeDir.get()==True):
                if (add_game(self.user_input.get(),r"~/"+self.filename.get())==True):
                    
                    messagebox.showinfo("Succes!","Succesfully added "+self.user_input.get())
         
            elif(self.isSteamVar.get()==True):
                if(add_steam_game(self.user_input.get(),self.filename.get())):
                     messagebox.showinfo("Succes!","Succesfully added "+self.user_input.get())
            else:
                if (add_game(self.user_input.get(),self.filename.get())==True):
                    messagebox.showinfo("Succes!","Succesfully added "+self.user_input.get())
                    
    def backup_window(self):
        self.filename=filedialog.askdirectory(title="Select a backup folder")
        a=backup(self.filename)
        messagebox.showinfo("Succes!","Succesfully backed up "+str(a)+" games")
    def remove_game_window(self):
        self.top=tk.Toplevel()
        self.user_input=tk.StringVar(self.top)
        self.top.title("Remove Game")
        self.top_label=tk.Label(text="Game name:",master=self.top,font=font_smaller)
        self.top_label.pack()
        self.top_text=tk.Entry(master=self.top,font=font_smaller,textvariable=self.user_input)
        self.top_text.pack()

        self.add = tk.Button(self.top, text="Remove Game", command=self.remove_game,width=20,font=font_smaller)
        self.add.pack()
        self.top_button_dismiss=tk.Button(self.top,text="Dismiss",command=self.top.destroy,font=font_smaller,width=20, fg="red")
        self.top_button_dismiss.pack()
    def remove_game(self):
        a=self.user_input.get()
        if(remove_game(self.user_input.get())==True):
              messagebox.showinfo("Succes!","Succesfully removed game "+str(a))

        else:
              messagebox.showerror("Error","Couldn't find game "+str(a))
    def restore_game(self):
        self.title="Select backup folder"
        self.top=tk.Toplevel()
        self.user_input=tk.StringVar(self.top)
        self.top.title("Restore Game")
        self.top_label=tk.Label(text="Game name:",master=self.top,font=font_smaller)
        self.top_label.pack()
        self.top_text=tk.Entry(master=self.top,font=font_smaller,textvariable=self.user_input)
        self.top_text.pack()

        self.add = tk.Button(self.top, text="Restore Game", command=self.restore_one_game,width=20,font=font_smaller)
        self.add.pack()
        self.top_button_dismiss=tk.Button(self.top,text="Dismiss",command=self.top.destroy,font=font_smaller,width=20, fg="red")
        self.top_button_dismiss.pack()
    def restore_one_game(self):
        self.filename=None
        self.get_folder()
        
        if (self.user_input.get()==""):
            messagebox.showerror("Error","You haven't entered a game name")
        elif(self.filename==None):
            messagebox.showerror("Error","You haven't selected a save folder")
        elif(os.path.isdir(self.filename+r"/"+self.user_input.get())==False):
            messagebox.showerror("Error","Can't find you game "+self.user_input.get())
        else:
            if(restore(self.user_input.get(),self.filename)==True):
                messagebox.showinfo("Succes!","Succesfully recovered the game "+self.user_input.get())
    def donate(self):
        webbrowser.open_new_tab("https://paypal.me/joshuasarlette")
    def github(self):
        webbrowser.open_new_tab("https://github.com/Joshi234/game-backer")
    def restore_all_games(self):
        a=0
        self.filename=None
        self.get_folder()
        if(self.filename==None):
            messagebox.showerror("Error","You haven't selected a save folder")
        else:
            backup_dir=self.filename
            for i in game_list:
                if(os.path.isdir(backup_dir+r'/'+i)):
                    
                    restore(i,backup_dir)
                    a=a+1
            messagebox.showinfo("Succes!","Succesfully recovered "+a+" games")
    def restore_all_games_window(self):
        
        self.top=tk.Toplevel()

        self.top.title("You sure?")
        self.top_label=tk.Label(text="Are you sure you want recover all game saves?\n THIS OVERWRITTES EVERY GAME SAVE AND CAN BREAK STUFF",master=self.top,font=font_smaller)
        self.top_label.pack()
        self.add = tk.Button(self.top, text="Restore Games", command=self.restore_all_games,width=20,font=font_smaller)
        self.add.pack()
        self.top_button_dismiss=tk.Button(self.top,text="Dismiss",command=self.top.destroy,font=font_smaller,width=20, fg="red")
        self.top_button_dismiss.pack()
    def about_window(self):
        self.top=tk.Toplevel()

        self.top.title("About")
        self.top_label=tk.Label(text="Creator: Joshi234\nI'm not responsible for any potential damage that can happen with this program.\nIf you want to contribute,\n you can add games and then do a pull request on github with the game_list.json\n that you can find in the same directory as this program.\nIf you aren't so in this github thing you can send it on\ndiscord to Joshi234#9828.",master=self.top,font=font_smaller)
        self.top_label.pack()
        self.top_button_donate=tk.Button(self.top,text="Support me by donating",command=self.donate,font=font_smaller,width=20, fg="orange")
        self.top_button_donate.pack()
        self.top_button_donate=tk.Button(self.top,text="Open Github page",command=self.github,font=font_smaller,width=20,)
        self.top_button_donate.pack()

        self.top_button_dismiss=tk.Button(self.top,text="Dismiss",command=self.top.destroy,font=font_smaller,width=20, fg="red")
        self.top_button_dismiss.pack()
    def create_widgets(self):
        self.menubar=tk.Menu(self.master)
        self.optionsMenu=tk.Menu(self.menubar)
        self.optionsMenu.add_command(label="Update game list",command=self.update_game_list_window,font=font_smaller)
        self.optionsMenu.add_command(label="Add game",command=self.add_game_window,font=font_smaller)
        self.optionsMenu.add_command(label="Remove game",command=self.remove_game_window,font=font_smaller)
        self.optionsMenu.add_command(label="Restore one game",command=self.restore_game,font=font_smaller)
        self.optionsMenu.add_command(label="Restore every game",command=self.restore_all_games_window,font=font_smaller)
        self.menubar.add_cascade(label="Actions",menu=self.optionsMenu,font=font_smaller)
        self.menubar.add_cascade(label="Options",command=self.options_window,font=font_smaller)
        self.menubar.add_cascade(label="About",command=self.about_window,font=font_smaller)
        self.master.config(menu=self.menubar)
        self.hi_there = tk.Button(self,width=20,height=4,font=font)

        self.hi_there["text"] = "Backup"
        self.hi_there["command"] = self.backup_window
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy ,width=20,font=font)
        self.quit.pack(side="bottom")

root = tk.Tk()
app = Application(master=root)
app.mainloop()

while 0==1:
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