import os

from dataclasses import dataclass
from datetime import datetime

from LogFileHandling import FileGetter, FileSaver
from LogEntry_dataclass import LogEntry
from LogCreateEntry import Transac, Liabili, Savings
from LogCreateEntry import CreateEntry
# from debugger import debug


# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "MAIN_AUDIT_LOG.csv"
DEFAULT_FILE_PATH:str = os.path.join(os.path.dirname(__file__), DEFAULT_FILE_NAME)



# MAIN CLASS - OVERHAULED
class Auditing(LogEntry):
    mainLogList:list = []
    currLoglist:list = []

    def __str__(self) -> str:
        return str(self.count)

    def __init__(self) -> None:
        ''' Program Startup sequence '''
        self.date = self.get_current_date()
        Auditing.mainLogList = FileGetter.fetch_saved_database(path=DEFAULT_FILE_PATH)
        Auditing.currLoglist = FileGetter.fetch_curr_list(dateToday=self.date)

    # OBJECT MANIPULATION
    def create_entry(self) -> object:
        ''' Takes in user input to dynamically and automatically make entry data details '''

        # FETCHING ENTRY DETAILS
        CreateEntry.fetch_entry_details()

        self.count   = self.get_total_entry_count()
        try: self.day= self.get_day(Auditing.mainLogList[-1].day)
        except IndexError: self.day = 1
        self.date    = self.get_current_date()        
        self.logType = CreateEntry.logType
        self.subtype = CreateEntry.subtype
        self.title   = CreateEntry.title
        self.amount  = CreateEntry.fetch_amount()
        self.logID   = CreateEntry.create_ID(self.count, self.logType, self.subtype, self.date)

        # CHECKS DUPLICATES AND GENERIC TITLES
        self.title = Auditing.title_handling(self.title)

        # ENTRY SAVING
        entry = LogEntry(
                    count=self.count,
                    day=self.day,
                    date=self.date,
                    logType=self.logType,
                    subtype=self.subtype,
                    title=self.title,
                    amount=self.amount,
                    logID=self.logID
                ) 
        Auditing.mainLogList.append(entry)
        Auditing.currLoglist.append(entry)
        FileSaver.save_and_append_data(entry.__dict__, DEFAULT_FILE_PATH)

    
    def modify_entry(self) -> LogEntry:
        print("^^^ Choose an entry to modify ^^^")
        searched_index:int = Auditing.search_entry()
        
        if searched_index == None:
            print("Entry not found. stopping modification process...\n")
            return
        
        moddedEntry:object = Auditing.mainLogList[searched_index]

        user_input:str = None
        while user_input not in ['A','B','C','D']:
            user_input = input("Choose data to modify:\n\tA. \'LogType\'\n\tB. \'Subtype\'\n\tC. \'Title\'\n\tD. \'Amount\'\n   > ").strip().upper()

            match user_input:
                case 'A':
                    CreateEntry.fetch_entry_details()
                    moddedEntry.logType = CreateEntry.logType
                    moddedEntry.subtype = CreateEntry.subtype
                    moddedEntry.title   = CreateEntry.title
                case 'B':
                    if moddedEntry.logType == "tra":
                        moddedEntry.subtype = Transac.get_log_subtype()

                    elif moddedEntry.logType == "lia":
                        moddedEntry.subtype = Liabili.get_log_subtype()
                        moddedEntry.title   = Liabili.get_log_title_from_subtype()
                    
                    elif moddedEntry.logType == "sav":
                        moddedEntry.subtype = Savings.get_log_subtype()
                        moddedEntry.title   = Savings.get_log_title_from_subtype()
                    
                    else:
                        print("\nMODIFYING_SUBTYPE_ERROR\n")
                case 'C':
                    print(f"Previous title: \'{moddedEntry.title}\'\n")
                    moddedEntry.title = input("Input new Entry Title\n   > ").strip()
                case 'D':
                    print(f"Previous amount: \'{moddedEntry.amount}\'\n")
                    moddedEntry.amount = CreateEntry.fetch_amount()
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

        moddedEntry.title = Auditing.title_handling(moddedEntry.title)
        moddedEntry.logID = CreateEntry.create_ID(moddedEntry.count, moddedEntry.logType, moddedEntry.subtype, moddedEntry.date)

        print("Entry has been modified. Save changes to update the CSV file.")
        Auditing.display_single_entry(moddedEntry, show_header=True)


    @classmethod
    def delete_entry(cls) -> None:
        print("\n!!! YOU ARE CURRENTLY IN THE PROCESS OF DELETING AN ENTRY !!!\n")
        searched_index:int = cls.search_entry()

        if searched_index == None:
            print("Entry not found. stopping deletion process...\n")
            return
        
        entry_to_be_deleted:object = cls.mainLogList[searched_index]

        cls.display_single_entry(entry_to_be_deleted, show_header=True)
        
        if input("Confirm Entry Deletion (\"yes\")\n\t> ").strip().lower() == "yes":
            cls.mainLogList.pop(searched_index)
            print(f"Entry has been succesfully deleted. Save changes to update the CSV file.")
        else:
            print(f"Stopping deletion process...\n")
            return
        
        # Fixing entry count jumps
        for i in range(searched_index, len(cls.mainLogList)):
            if cls.mainLogList[i].count != i:
                cls.mainLogList[i].count = i + 1


    # UTILS
    def get_total_entry_count(self) -> int:
        '''Fetches the count count of log Entries in the dynamic main list'''
        return len(Auditing.mainLogList) + 1
    
    def get_current_date(self) -> str:
        return datetime.now().strftime("%d-%m-%Y")

    def get_day(self, previousDay) -> int:
        if self.date != Auditing.mainLogList[-1].date:
            return previousDay + 1
        return previousDay
    
    @classmethod
    def title_handling(cls, title:str) -> str:
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
                return "{} 2".format(duplicateTitle)


        genericTitles = [ "Pamasahe", "Lost", "Found", "Random Magic Sorcery" ]
        excludedTitles= [ "Loaned", "Owed" ]

        if title in genericTitles and not " " in title:
            title = "{} 1".format(title)

        for entry in cls.currLoglist:
            if entry.title == title and title not in excludedTitles:
                print(f"Duplicate title \'{title}\' found, adding...")
                title =  add_title_count(title)

        return title
    

    @classmethod
    def save_all_entries(cls) -> None:
        for entry in cls.mainLogList:
            FileSaver.save_all_data(cls.mainLogList, DEFAULT_FILE_PATH)
    
    @classmethod
    def display_single_entry(cls, entry, show_header=False) -> None:
        if show_header == True:
            print(f"COUNT\tDAY\tDATE\t\tTYPE\tSUBTYPE\tTITLE\t\t\tAMOUNT\t\tLOG ID")
            print(f"{entry.count}\t{entry.day}\t{entry.date}\t{entry.logType}\t{entry.subtype}\t{entry.title:<20}\t{entry.amount:<15}\t{entry.logID}")
        else:
            print(f"{entry.count}\t{entry.day}\t{entry.date}\t{entry.logType}\t{entry.subtype}\t{entry.title:<20}\t{entry.amount:<15}\t{entry.logID}")            
                
    @classmethod
    def display_entries(cls, specified=False, search_parameter=None) -> None:
        max_display_limit = 100
        for entry in cls.mainLogList[-max_display_limit-1:]:
            if not specified:
                cls.display_single_entry(entry)
            elif search_parameter in entry.logType or search_parameter in entry.subtype:
                cls.display_single_entry(entry)

    @classmethod
    def search_entry(cls) -> int:
        ''' Returns index of searched entry based on the main log list '''

        user_input:str = None
        while True:
            user_input = input("What log type to search for? (tra/lia/sav) (debi/cred/loan/owed/depo/with) (\'back\' to return): ").strip().lower()

            if user_input == "back":
                return
            elif user_input not in ["tra","lia","sav",  "debi","cred","loan","owed","depo","with"]:
                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")
                continue

            break

        cls.display_entries(specified=True, search_parameter=user_input)

        while True:
            user_input = input("Enter the logID: ").strip()
            
            for entry in cls.mainLogList:
                if entry.logID == user_input:
                    return cls.mainLogList.index(entry)
            
            print(f"ID of \'{user_input}\' not found")
            return








if __name__ == '__main__':
    audit = Auditing()
    while True: 
        audit.create_entry()
        print(f"ENTRY FOUND: {audit.search_entry()}")
        audit.delete_entry()
        audit.modify_entry()
        audit.save_all_entries()
        audit.display_entries()
        if input("exit? [y/n]: ").lower() == 'y':
            break
