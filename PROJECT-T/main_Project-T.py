from LogFileHandling import FileGetter, FileSaver
from LogEntry_dataclass import LogEntry
from LogDetails import Transac, Liabili, Savings
from debugger import debug

from dataclasses import dataclass
from datetime import datetime
import os

# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "AUDIT_LOG.csv"
DEFAULT_FILE_PATH:str = os.path.join(__file__[0:-len(os.path.basename(__file__))], DEFAULT_FILE_NAME)

''' NOTES: CREATE A SINGLE LIST THAT IS SAVED, AND HAVE SPECIFIC FUNCTIONS 
    TO SEGREGATE EACH ENTRY INTO THEIR OWN RESPECTIVE LOG TYPES AND SUBTYPE 
    DATA STOP MESSING AROUND WITH CSV, JSON, PY FILE HANDLING, FOCUS ON ONE '''



# MAIN CLASS - OVERHAULED
class Auditing(LogEntry):
    mainLogList:list = []
    currLoglist:list = []

    def __init__(self) -> None:
        self.startup()

    def __str__(self) -> str:
        return str(self.total)


    def startup(self) -> None:
        self.check_date_change()
        Auditing.mainLogList = FileGetter.fetch_saved_database(DEFAULT_FILE_PATH)
        Auditing.currLoglist = self.get_curr_list()


    def add_entry(self) -> None:
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


    def get_curr_list(self) -> list:
        currentList = []
        for obj in Auditing.mainLogList:
            if obj.date == self.date:
                currentList.append(obj)
        return currentList
    
    def check_date_change(self) -> None:
        tempDate = datetime.now().strftime('%d-%m-%Y')
        if not self.date == tempDate:
            self.date = tempDate

    def set_changed_date(self) -> None:
        self.date = datetime.now().strftime("%d-%m-%Y")


    

    def create_entry(self):
        # Auditing.temp_fetch_mainLog()

        def init_fetch_date() -> None:
            self.date = datetime.now().strftime('%d-%m-%Y')

        def init_fetch_entry_details() -> None:
            ''' Fetches info for LOGTYPE, Log SUBTYPE, and TITLE '''

            def add_title_count(duplicateTitle) -> None:
                ''' Adds an increasing number to a duplicate/generic title '''

                if " " in duplicateTitle and (duplicateTitle[-1]):
                    duplicateTitle = duplicateTitle.split(" ")
                    try:
                        duplicateTitle[-1] = str(int(duplicateTitle[-1]) + 1)
                    except ValueError or BaseException as e:
                        print(f"TITLE_ADDITION_ERROR:\n\t{e}")
                    finally: 
                        self.title = " ".join(duplicateTitle)
                else:
                    self.title = "{} 1".format(duplicateTitle)


            def check_generic_title() -> None:
                genericTitles = [ "Pamasahe", "Found", "Lost", "Deposit", "Withdrawal", "Random Magic Sorcery" ]
                if self.title in genericTitles and not " " in self.title:
                    add_title_count(self.title)

            def check_title_duplicates() -> None:
                # excludedTitles = [ "Loaned", "Owed"]
                for obj in Auditing.currLoglist:
                    if self.title == obj.title:
                        debug(f"{obj = }")
                        debug(f"{obj.logID = }")
                        debug(f"{self.title = } == {obj.title = }, ")
                        print(f"Duplicate title \'{self.title}\' found, adding...")
                        add_title_count(self.title)


            # Start of fetch details function 
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

                check_generic_title()
                check_title_duplicates()
            # END OF INIT_FETCH_ENTRY_DETAILS


        def init_fetch_amount() -> None:
            self.amount = 0
            while self.amount == 0:
                try: self.amount = abs(float(input("Input Transaction Amount: ")))
                except ValueError as e: print(f"NaN_ERROR: {e}")

        def init_fetch_total_count() -> None:
            self.total = len(Auditing.mainLogList) + 1

        def init_create_ID() -> None:
            self.logID = f"{self.total}//{self.logType}//{self.subtype}//{self.date}"

        
        # FUNCTION CALLS
        init_fetch_date()
        init_fetch_entry_details()
        init_fetch_amount()
        init_fetch_total_count()
        init_create_ID()

        self.add_entry()
        FileSaver.save_data(self.__dict__, DEFAULT_FILE_PATH)

        return self
    # END OF CREATE_ENTRY


    @classmethod
    def display_all_entries(cls) -> bool:
        if len(cls.mainLogList) < 100:  # temp_max_limit
            for obj in cls.mainLogList:
                print(f"{obj}")

    @classmethod
    def get_total_entry_count(cls) -> int:
        return len(cls.mainLogList) + 1

    @classmethod
    def get_main_list(cls) -> list:
        return cls.mainLogList
    



if __name__ == '__main__':
    prog_input:str = ''

    audit = Auditing()

    while prog_input not in ['y']:
        audit.create_entry()

        prog_input = input("exit? [y/n]: ").lower()    

        debug()
        debug(f"{Auditing.mainLogList = }")
        debug()
        audit.display_all_entries()
        debug("end.")