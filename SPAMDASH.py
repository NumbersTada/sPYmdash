import requests,tkinter,time,customtkinter,base64,hashlib,webbrowser,random,pygame,os,urllib.request,tkinter.messagebox
from threading import Thread
from itertools import cycle
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
pygame.init()
def commentCHK(*,username,comment,levelid,percentage,type):
        part1 = username + comment + levelid + str(percentage) + type + "xPT6iUrtws0J"
        return base64.b64encode(xor(hashlib.sha1(part1.encode()).hexdigest(),"29481").encode()).decode()
def xor(data, key):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
def gjpEncrypt(data):
        return base64.b64encode(xor(data,"37526").encode()).decode()
def gjpDecrypt(data):
        return xor(base64.b64decode(data.encode()).decode(),"37526")
def getGJUsers(target):
    data={
        "secret":"Wmfd2893gb7",
        "str":target
    }
    request = requests.post("http://www.boomlings.com/database/getGJUsers20.php",data=data,headers={"User-Agent": ""}).text.split(":")[1::2]
    username = request[0]
    uuid = request[2]
    accountid = request[10]
    return (username,accountid,uuid)
def uploadGJComment(name,passw,comment,perc,level):
    try:
            accountid = getGJUsers(name)[1]                                                                                                                        
            gjp = gjpEncrypt(passw)
            c = base64.b64encode(comment.encode()).decode()
            chk = commentCHK(username=name,comment=c,levelid=str(level),percentage=perc,type="0")
            data={
                "secret":"Wmfd2893gb7",
                "accountID":accountid,
                "gjp":gjp,
                "userName":name,
                "comment":c,
                "levelID":level,
                "percent":perc,
                "chk":chk
            }
            return requests.post("http://www.boomlings.com/database/uploadGJComment21.php",data=data,headers={"User-Agent": ""}).text
    except:
            return "error"
def fetchID():
    data={
        "gameVersion":"21",
        "binaryVersion":"35",
        "gdw":"0",
        "type":"4",
        "str":"",
        "diff":"-",
        "len":"-",
        "page":"0",
        "total":"0",
        "uncompleted":"0",
        "onlyCompleted":"0",
        "featured":"0",
        "original":"0",
        "twoPlayer":"0",
        "coins":"0",
        "epic":"0",
        "secret":"Wmfd2893gb7"
    }
    fetched = requests.post("http://www.boomlings.com/database/getGJLevels21.php",data=data,headers={"User-Agent": ""}).text
    return fetched.split(":")[1]
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        try:
            with open(os.path.expanduser("~")+"\\AppData\\Local\\SPAMDASH\\config.dat",mode="r",encoding="utf-8") as rconfig:
                file=rconfig.read()
                username=file.split("•")[0]
                password=file.split("•")[1]
                accid=file.split("•")[2]
                comment=file.split("•")[3]
                percentage=file.split("•")[4]
                delay=file.split("•")[5].split("\n")[0]
        except:
            os.mkdir(os.path.expanduser("~")+"\\AppData\\Local\\SPAMDASH\\")
            with open(os.path.expanduser("~")+"\\AppData\\Local\\SPAMDASH\\config.dat",mode="w",encoding="utf-8") as rconfig:
                print("•••••",file=rconfig)
        def startBot():
            Thread(target=botter).start()
        def botter():
            self.startButton.configure(state="disabled")
            progress = 0
            username = self.entry1.get()
            password = self.entry2.get()
            accid = self.entry3.get()
            comment = self.entry.get()
            percentage = int(self.entry5.get())
            delay = int(self.entry4.get())
            with open(os.path.expanduser("~")+"\\AppData\\Local\\SPAMDASH\\config.dat",mode="w",encoding="utf-8") as sconfig:
                print(username+"•"+password+"•"+str(accid)+"•"+comment+"•"+str(percentage)+"•"+str(delay),file=sconfig)
            while True:
                self.progressbar.configure(mode="determinate")
                self.progresslabel.configure(text="Uploading comment...")
                self.progressbar.stop()
                while progress <= 1:
                    self.progressbar.set(progress)
                    progress += 0.1
                    time.sleep(0.01)
                levelID = fetchID()
                response = str(uploadGJComment(username,password,comment,percentage,levelID))
                if response == "":
                    self.progresslabel.configure(text="A problem has occured. "+response)
                elif response == "-1":
                    self.progresslabel.configure(text="A problem has occured. "+response)
                elif response == "error code: 1005":
                    self.progresslabel.configure(text="A problem has occured. "+response)
                else:
                    self.progresslabel.configure(text="Comment uploaded on "+levelID+" (comment ID: "+response+")")
                time.sleep(2)
                self.progresslabel.configure(text="Waiting...")
                self.progressbar.configure(mode="indeterminate")
                self.progressbar.start()
                time.sleep(28)
        self.title("SPAMDASH")
        self.geometry(f"{900}x{450}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebarFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebarFrame, text="SPAMDASH", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebarFrame, command=self.openWebsite, text="GitHub")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebarFrame, command=self.meow, text="Meow")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebarFrame, text="Vzhled:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appereanceMenu = customtkinter.CTkOptionMenu(self.sidebarFrame, values=["Light (bruh)", "Dark", "System"],command=self.changeTheme)
        self.appereanceMenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scalingLabel = customtkinter.CTkLabel(self.sidebarFrame, text="Velikost:", anchor="w")
        self.scalingLabel.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scalingMenu = customtkinter.CTkOptionMenu(self.sidebarFrame, values=["80%", "90%", "100%", "110%", "120%"],command=self.changeScaling)
        self.scalingMenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Comment")
        self.entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        if comment != "":
            self.entry.insert(0,comment)
        else:
            pass
        self.startButton = customtkinter.CTkButton(master=self, text="Start", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=startBot)
        self.startButton.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Account Info")
        self.tabview.add("Comment Settings")
        self.tabview.tab("Account Info").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Comment Settings").grid_columnconfigure(0, weight=1)
        self.entry1 = customtkinter.CTkEntry(self.tabview.tab("Account Info"), placeholder_text="Username")
        self.entry1.grid(row=1, column=0, padx=20, pady=(10, 10))
        if username != "":
            self.entry1.insert(0,username)
        else:
            pass
        self.entry2 = customtkinter.CTkEntry(self.tabview.tab("Account Info"), placeholder_text="Password", show="•")
        self.entry2.grid(row=2, column=0, padx=20, pady=(10, 10))
        if password != "":
            self.entry2.insert(0,password)
        else:
            pass
        self.entry3 = customtkinter.CTkEntry(self.tabview.tab("Account Info"), placeholder_text="Account ID")
        self.entry3.grid(row=3, column=0, padx=20, pady=(10, 10))
        if accid != "":
            self.entry3.insert(0,accid)
        else:
            pass
        self.accidButton = customtkinter.CTkButton(self.tabview.tab("Account Info"), command=self.getid, text="Get Account ID and Insert")
        self.accidButton.grid(row=4, column=0, padx=20, pady=10)
        self.labelTab2 = customtkinter.CTkLabel(self.tabview.tab("Comment Settings"), text="Delay should be at least 30 seconds.")
        self.labelTab2.grid(row=0, column=0, padx=20, pady=20)
        self.entry4 = customtkinter.CTkEntry(self.tabview.tab("Comment Settings"), placeholder_text="Delay")
        self.entry4.grid(row=1, column=0, padx=20, pady=(10, 10))
        if delay != "":
            self.entry4.insert(0,delay)
        else:
            pass
        self.entry5 = customtkinter.CTkEntry(self.tabview.tab("Comment Settings"), placeholder_text="Percentage")
        self.entry5.grid(row=2, column=0, padx=20, pady=(10, 10))
        if percentage != "":
            self.entry5.insert(0,percentage)
        else:
            pass
        self.progressbarFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.progressbarFrame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.progressbarFrame.grid_columnconfigure(0, weight=1)
        self.progressbarFrame.grid_rowconfigure(4, weight=1)
        self.progresslabel = customtkinter.CTkLabel(self.progressbarFrame, font=customtkinter.CTkFont(size=12), text="Bot is not running")
        self.progresslabel.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.progressbar = customtkinter.CTkProgressBar(self.progressbarFrame)
        self.progressbar.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.checkboxFrame = customtkinter.CTkFrame(self)
        self.checkboxFrame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.autoStats = customtkinter.CTkCheckBox(master=self.checkboxFrame, text="AutoStats (WIP)")
        self.autoStats.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.autoStats.configure(state="disabled")
        self.randomComment = customtkinter.CTkCheckBox(master=self.checkboxFrame, text="Random Comments (WIP)")
        self.randomComment.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.randomComment.configure(state="disabled")

        self.appereanceMenu.set("Dark")
        self.scalingMenu.set("100%")
        self.progressbar.set(0)
    def getid(self):
        self.entry3.insert(0,getGJUsers(self.entry1.get())[1])
    def changeTheme(self, newMode: str):
        if newMode == "Light (bruh)":
            customtkinter.set_appearance_mode("light")
        if newMode == "Dark":
            customtkinter.set_appearance_mode("dark")
        if newMode == "System":
            customtkinter.set_appearance_mode("system")
    def changeScaling(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    def meow(self):
        if not os.path.exists(os.path.expanduser("~")+"\\AppData\\Local\\SPAMDASH\\meow.mp3"):
            urllib.request.urlretrieve("http://www.tadaprograms.com/meow.mp3",os.path.expanduser("~")+"\\AppData\\Local\\SPAMDASH\\meow.mp3")
        pygame.mixer.Sound(os.path.expanduser("~")+"\\AppData\\Local\\SPAMDASH\\meow.mp3").play()
    def openWebsite(self):
        webbrowser.open("https://github.com/NumbersTada/sPYmdash")
if __name__ == "__main__":
    app = App()
    app.mainloop()
