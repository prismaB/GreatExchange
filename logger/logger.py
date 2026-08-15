import sqlite3 
import json
import threading
import datetime
from pathlib import Path as p
class Logger:
    log = {
    "DateTime":None,
    "error":None
    }
    def __init__(self,dateTime,Error) -> None:
        self.dateTime = dateTime
        self.error = Error
    def DbConnect(self) -> None:
        path = p.cwd()
        print(path)
    def logType(self) -> str:
        pass

if __name__ == "__main__":
    a = Logger()
    Logger.DbConnect()