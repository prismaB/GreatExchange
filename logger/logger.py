import sqlite3
import threading
import queue
from datetime import datetime
from pathlib import Path as p
import json
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

class Logger:
    def __init__(self,dbpath=""):
        self.__dbpath = dbpath
        self.__dbpath = "Great.db"
        self.datetime = datetime
        # self.Service =Service
        self.datetime = datetime.now()
        self.Service =""
    def Dbdirectory(self):
        MODULE_DIR = p(__file__).resolve().parent
        self.__dbpath = p("config.json")
        config_loc = MODULE_DIR.parent / "config.json"
        try:
            with open(config_loc,"r",encoding='utf-8') as file:
                configData = json.load(file)
                logDirectory =p.cwd() / configData["Directory"]["directory"]
                if logDirectory.exists():print("{GREEN}exist")
                else:
                    print(f"{RED}log directory not found.{RESET}")
                    print(f"{YELLOW}we create the log directory{RESET}")
                    try:
                        p.mkdir(logDirectory)
                        if logDirectory.exists():print("{GREEN}exist")
                        else:print(f"{RED}log directory not found.{RESET}")
                    except PermissionError:
                        print("{RED}Permisson denied.Try with sudo{RESET}")
        except FileNotFoundError:
            pass #ekleyeceğim