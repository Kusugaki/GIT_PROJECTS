import os

from dataclasses import dataclass
from datetime import datetime

from LogFileHandling import FileGetter, FileSaver
from LogEntry_dataclass import LogEntry
from LogDetails import Transac, Liabili, Savings
from LogCreateEntry import CreateEntry
from debugger import debug


# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "AUDIT_LOG.csv"
DEFAULT_FILE_PATH:str = os.path.join(os.path.dirname(__file__), DEFAULT_FILE_NAME)



# MAIN CLASS - OVERHAULED
class Auditing(LogEntry):
    mainLogList:list = []
    currLoglist:list = []

    def __str__(self) -> str:
        return str(self.total)

    def __init__(self) -> None:
        ''' Program Startup sequence '''
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
        '''Fetches the total count of log Entries in the dynamic main list'''
        return len(Auditing.mainLogList) + 1
    
    def get_current_date(self) -> str:
        return datetime.now().strftime("%d-%m-%Y")
    
    def check_date_change(self) -> bool:
        return self.date == datetime.now().strftime('%d-%m-%Y')


    def create_entry(self) -> object:
        ''' Takes in user input to dynamically and automatically make entry data details '''

        # FETCHING ENTRY DETAILS
        CreateEntry.fetch_entry_details()

        self.total   = self.get_total_entry_count()
        self.date    = self.get_current_date()        
        self.logType = CreateEntry.logType
        self.subtype = CreateEntry.subtype
        self.title   = CreateEntry.title
        self.amount  = CreateEntry.fetch_amount()
        self.logID   = CreateEntry.create_ID(self.total, self.logType, self.subtype, self.date)


        def add_title_count(duplicateTitle) -> None:
            '''Adds an increasing number to a duplicate/generic title'''

            if " " in duplicateTitle:
                parts = duplicateTitle.split(" ")
                try:
                    parts[-1] = str(int(parts[-1]) + 1)
                except ValueError or BaseException as e:
                    print(f"TITLE_ADDITION_ERROR:\n\t{e}")
                finally: 
                    return " ".join(parts)
            else:
                return "{} 1".format(duplicateTitle)

        # TITLE HANDLING
        genericTitles = [ "Pamasahe", "Found", "Lost", "Deposit", "Withdrawal", "Random Magic Sorcery" ]
        excludedTitles= [ "Loaned", "Owed" ]

        if self.title in genericTitles and not " " in self.title:
            self.title = add_title_count(self.title)

        for obj in Auditing.currLoglist:
            if self.title == obj.title and self.title not in excludedTitles:
                print(f"Duplicate title \'{self.title}\' found, adding...")
                self.title = add_title_count(self.title)

        # ENTRY SAVING
        self.__append_entry()
        FileSaver.save_data(self.__dict__, DEFAULT_FILE_PATH)
        
        return self





    def __append_entry(self) -> None:
        ''' Appends created entry'''
        Auditing.mainLogList.append(
            LogEntry(
                total=self.total,
                date=self.date,
                logType=self.logType,
                subtype=self.subtype,
                title=self.title,
                amount=self.amount,
                logID=self.logID
            )
        )





    @classmethod
    def display_all_entries(cls) -> bool:
        if len(cls.mainLogList) < 100:  # temp_max_limit
            for obj in cls.mainLogList:
                print(f"{obj}")



if __name__ == '__main__':
    audit = Auditing()
    while True: 
        audit.create_entry()
        audit.display_all_entries()
        if input("exit? [y/n]: ").lower() == 'y':
            break
