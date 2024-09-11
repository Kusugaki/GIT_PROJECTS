import os

from dataclasses import dataclass
from datetime import datetime

from LogFileHandling import FileGetter, FileSaver
from LogEntry_dataclass import LogEntry
from LogDetails import Transac, Liabili, Savings
from debugger import debug
from CreateEntry import CreateEntry

# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "AUDIT_LOG.csv"
DEFAULT_FILE_PATH:str = os.path.join(os.path.dirname(__file__), DEFAULT_FILE_NAME)

''' NOTES: CREATE A SINGLE LIST THAT IS SAVED, AND HAVE SPECIFIC FUNCTIONS 
    TO SEGREGATE EACH ENTRY INTO THEIR OWN RESPECTIVE LOG TYPES AND SUBTYPE 
    DATA STOP MESSING AROUND WITH CSV, JSON, PY FILE HANDLING, FOCUS ON ONE '''



# MAIN CLASS - OVERHAULED
class Auditing(LogEntry):
    mainLogList:list = []
    currLoglist:list = []

    def __str__(self) -> str:
        return str(self.total)

    def __init__(self) -> None:
        if self.check_date_change():
            self.date = self.get_current_date()
        Auditing.mainLogList = FileGetter.fetch_saved_database(DEFAULT_FILE_PATH)
        Auditing.currLoglist = self.get_curr_list()


    def get_curr_list(self) -> list[LogEntry]:
        currentList = []
        for obj in Auditing.mainLogList:
            if obj.date == self.date:
                currentList.append(obj)
        return currentList
    
    def get_total_entry_count(self) -> int:
        return len(Auditing.mainLogList) + 1
    

    def get_current_date(self) -> str:
        return datetime.now().strftime("%d-%m-%Y")
    
    def check_date_change(self) -> bool:
        return self.date == datetime.now().strftime('%d-%m-%Y')


    def create_entry(self) -> object:
        ''' Takes in user input to dynamically and automatically make entry data details '''

        # FUNCTION CALLS
        self.date = self.get_current_date()
        CreateEntry.init_fetch_entry_details()
        # self.logType = 
        # self.subtype =
        # self.title = 
        self.amount = CreateEntry.init_fetch_amount()
        self.total = CreateEntry.init_fetch_total_count()
        self.logID = CreateEntry.init_create_ID()

        if self.__check_generic_title():
            self.__add_title_count(self.title)
        self.__check_title_duplicates()
        self.__append_entry()
        FileSaver.save_data(self.__dict__, DEFAULT_FILE_PATH)
        
        return self



    def __check_generic_title(self) -> bool:
        genericTitles = [ "Pamasahe", "Found", "Lost", "Deposit", "Withdrawal", "Random Magic Sorcery" ]
        return self.title in genericTitles and not " " in self.title

    def __check_title_duplicates(self) -> None:
        excludedTitles= ["Loaned", "Owed"]
        for obj in Auditing.currLoglist:
            if self.title == obj.title and self.title not in excludedTitles:
                print(f"Duplicate title \'{self.title}\' found, adding...")
                self.__add_title_count(self.title)

    def __add_title_count(self, duplicateTitle) -> None:
        '''Adds an increasing number to a duplicate/generic title'''

        if " " in duplicateTitle:
            parts = duplicateTitle.split(" ")
            try:
                parts[-1] = str(int(parts[-1]) + 1)
            except ValueError or BaseException as e:
                print(f"TITLE_ADDITION_ERROR:\n\t{e}")
            finally: 
                self.title = " ".join(parts)
        else:
            self.title = "{} 1".format(duplicateTitle)



    def __append_entry(self) -> None:
        ''' Appends created entry'''
        if Auditing.mainLogList[-1].date == entry.date:
            Auditing.currLoglist.append(entry)
        else:
            debug("Date has changed.")
            self.date = self.get_current_date()

        entry = LogEntry(
            total=self.total,
            date=self.date,
            logType=self.logType,
            subtype=self.subtype,
            title=self.title,
            amount=self.amount,
            logID=self.logID
        )
        Auditing.mainLogList.append(entry)





    @classmethod
    def display_all_entries(cls) -> bool:
        if len(cls.mainLogList) < 100:  # temp_max_limit
            for obj in cls.mainLogList:
                print(f"{obj}")




details: dict[dict[dict[dict[str]]]] = {
    "LogType": {
        "Transac": {
             "subtype": {
                "Debit":"debi",
                "Credit":"cred"
            }
        },
        "Liabili": {
            "subtype": {
                "Loaned":"loan",
                "Owed":"owed"
            }
        },
        "Savings": {
            "subtype": {
                "Deposit":"depo",
                "Withdrawal":"draw"
            }
        }
    }
}

if __name__ == '__main__':
    audit = Auditing()
    while True: 
        audit.create_entry()
        audit.display_all_entries()
        if input("exit? [y/n]: ").lower() == 'y':
            break