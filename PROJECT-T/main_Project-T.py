import os

from dataclasses import dataclass
from datetime import datetime

from LogFileHandling import FileGetter, FileSaver
from LogEntry_dataclass import LogEntry
from LogDetails import Transac, Liabili, Savings
from debugger import debug


# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "AUDIT_LOG.csv"
DEFAULT_FILE_PATH:str = os.path.join(os.path.dirname(__file__), DEFAULT_FILE_NAME)


# MAIN CLASS - OVERHAULED
class Auditing(LogEntry):
    mainLogList:list = []
    currLoglist:list = []

    def __init__(self) -> None:
        self.__startup()

    def __str__(self) -> str:
        return str(self.total)

    def __startup(self) -> None:
        self.check_date_change()
        Auditing.mainLogList = FileGetter.fetch_saved_database(DEFAULT_FILE_PATH)
        Auditing.currLoglist = self.get_curr_list()

    def get_curr_list(self) -> list:
        currentList = []
        for obj in Auditing.mainLogList:
            if obj.date == self.date:
                currentList.append(obj)
        return currentList
    
    def get_total_entry_count(self) -> int:
        return len(Auditing.mainLogList) + 1
    
    def check_date_change(self) -> None:
        currentDate = datetime.now().strftime('%d-%m-%Y')
        if self.date != currentDate:
            self.date = currentDate

    def set_changed_date(self) -> None:
        self.date = datetime.now().strftime("%d-%m-%Y")

    def create_entry(self) -> object:
        ''' Takes in user input to dynamically and automatically make entry data details '''

        # FUNCTION CALLS
        self.__init_fetch_date()
        self.__init_fetch_entry_details()
        self.__init_fetch_amount()
        self.__init_fetch_total_count()
        self.__init_create_ID()

        self.__append_entry()
        FileSaver.save_data(self.__dict__, DEFAULT_FILE_PATH)
        
        return self
    

    def __init_fetch_date(self) -> None:
        self.set_changed_date()

    def __init_fetch_entry_details(self) -> None:
        '''Fetches info for LOGTYPE, Log SUBTYPE, and TITLE'''

        user_input = None
        while user_input not in ['A','B','C']:
            user_input = input("""Enter Log Type:\n\tA. \'Transactions\'\n\tB. \'Liabilities\'\n\tC. \'Savings\'\n  > """).upper()

            match user_input:
                case 'A':
                    Transac.fetch_entry_details()
                    self.logType = Transac.logType
                    self.subtype = Transac.subtype
                    self.title   = input("Input Log Title: ").strip()
                case 'B':
                    Liabili.fetch_entry_details()
                    self.logType = Liabili.logType
                    self.subtype = Liabili.subtype
                    self.title   = Liabili.titleChoice
                case 'C':
                    Savings.fetch_entry_details()
                    self.logType = Savings.logType
                    self.subtype = Savings.subtype
                    self.title   = Savings.titleChoice
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")
                    continue
        self.__check_generic_title()
        self.__check_title_duplicates()


    def __init_fetch_amount(self) -> None:
        self.__amount = 0
        while self.amount == 0:
            try: self.amount = abs(float(input("Input Transaction Amount: ")))
            except ValueError as e: print(f"NaN_ERROR: {e}")

    def __init_fetch_total_count(self) -> None:
        '''Fetches the total count of log Entries in the dynamic main list'''
        self.total = self.get_total_entry_count()

    def __init_create_ID(self) -> None:
        '''Creates a unique ID'''
        self.logID = f"{self.total}//{self.logType}//{self.subtype}//{self.date}"

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


    def __check_generic_title(self) -> None:
        genericTitles = [ "Pamasahe", "Found", "Lost", "Deposit", "Withdrawal", "Random Magic Sorcery" ]
        if self.title in genericTitles and not " " in self.title:
            self.__add_title_count(self.title)

    def __check_title_duplicates(self) -> None:
        excludedTitles= ["Loaned", "Owed"]
        for obj in Auditing.currLoglist:
            if self.title == obj.title and self.title not in excludedTitles:
                print(f"Duplicate title \'{self.title}\' found, adding...")
                self.__add_title_count(self.title)

    def __append_entry(self) -> None:
        ''' Appends created entry'''
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

        if Auditing.mainLogList[-1].date == entry.date:
            Auditing.currLoglist.append(entry)
        else:
            debug("Date has changed.")
            self.set_changed_date()

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
