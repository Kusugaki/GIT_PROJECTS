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
    def create_entry(self) -> int:
        ''' Takes in user input to dynamically and automatically make entry data details '''

        # FETCHING ENTRY DETAILS
        CreateEntry.fetch_entry_details()

        self.count   = self.get_total_entry_count()
        self.day     = self.get_day()
        self.date    = self.get_current_date()        
        self.logType = CreateEntry.logType
        self.subtype = CreateEntry.subtype
        self.title   = CreateEntry.title.title()
        self.amount  = CreateEntry.fetch_amount()
        self.logID   = CreateEntry.create_ID(self.count, self.logType, self.subtype, self.date)
        self.liaName = CreateEntry.liaName if self.logType == Liabili.logTypeDetail else "NON-LIA"

        # CHECKS DUPLICATES AND GENERIC TITLES
        self.title = Auditing.check_generic_or_duplicate_titles(self.title)

        # ENTRY SAVING
        entry = LogEntry(
                    count=self.count,
                    day=self.day,
                    date=self.date,
                    logType=self.logType,
                    subtype=self.subtype,
                    title=self.title,
                    amount=self.amount,
                    logID=self.logID,
                    liaName=self.liaName
                ) 
        Auditing.mainLogList.append(entry)
        Auditing.currLoglist.append(entry)
        FileSaver.save_and_append_data(entry.__dict__, DEFAULT_FILE_PATH)

        return 1

    
    def modify_entry(self) -> int:
        ''' (-) note: implementation of this could be / should be improved '''
        print("^^^ Choose an entry to modify ^^^")
        searched_index:int = Auditing.search_entry()
        
        if searched_index == None:
            print("Entry not found. stopping modification process...\n")
            return 0
        
        moddedEntry:object = Auditing.mainLogList[searched_index]

        user_input:str = None
        while user_input not in ['A','B','C','D']:
            user_input = input("Choose data to modify:\n\tA. \'LogType\'\n\tB. \'Subtype\'\n\tC. \'Title\'\n\tD. \'Amount\'\n   > ").strip().upper()

            match user_input:
                case 'A':   # Logtype
                    CreateEntry.fetch_entry_details()
                    moddedEntry.logType = CreateEntry.logType
                    moddedEntry.subtype = CreateEntry.subtype
                    if moddedEntry.logType == Liabili.logTypeDetail:
                        moddedEntry.liaName = Liabili.get_liable_entity(liable_subtype=moddedEntry.subtype)
                        moddedEntry.title   = Liabili.get_log_title_from_subtype(person=moddedEntry.liaName)
                    else:
                        moddedEntry.title   = CreateEntry.title
                case 'B':   # Subtype
                    if moddedEntry.logType == "tra":
                        moddedEntry.subtype = Transac.get_log_subtype()

                    elif moddedEntry.logType == "lia":
                        moddedEntry.subtype = Liabili.get_log_subtype()
                        moddedEntry.liaName = Liabili.get_liable_entity(liable_subtype=moddedEntry.subtype)
                        moddedEntry.title   = Liabili.get_log_title_from_subtype(person=moddedEntry.liaName)
                    
                    elif moddedEntry.logType == "sav":
                        moddedEntry.subtype = Savings.get_log_subtype()
                        moddedEntry.title   = Savings.get_log_title_from_subtype()
                    else:
                        print("\nMODIFYING_SUBTYPE_ERROR\n")
                case 'C':   # Title
                    print(f"Previous title: \'{moddedEntry.title}\'\n")
                    moddedEntry.title = input("Input new Entry Title\n   > ").strip()
                case 'D':   # Amount
                    print(f"Previous amount: \'{moddedEntry.amount}\'\n")
                    moddedEntry.amount = CreateEntry.fetch_amount()
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

        moddedEntry.title = Auditing.check_generic_or_duplicate_titles(moddedEntry.title)
        moddedEntry.logID = CreateEntry.create_ID(moddedEntry.count, moddedEntry.logType, moddedEntry.subtype, moddedEntry.date)

        print("Entry has been modified. Save changes to update the CSV file.")
        Auditing.display_single_entry(moddedEntry, show_header=True)


    @classmethod
    def delete_entry(cls) -> int:
        print("\n!!! YOU ARE CURRENTLY IN THE PROCESS OF DELETING AN ENTRY !!!\n")

        searched_index:int = cls.search_entry()

        if searched_index == None or searched_index == 0:
            print("Entry not found. stopping deletion process...\n")
            return 0

        entry_to_be_deleted:object = cls.mainLogList[searched_index]
        
        cls.display_single_entry(entry_to_be_deleted, show_header=True)
        
        if input("Confirm Entry Deletion (\"yes\")\n\t> ").strip().lower() == "yes":
            cls.mainLogList.pop(searched_index)
            print(f"Entry has been succesfully deleted. Save changes to update the CSV file.")
        else:
            print(f"Stopping deletion process...\n")
            return 0
        
        # Fixing entry count jumps
        for i in range(searched_index, len(cls.mainLogList)):
            if cls.mainLogList[i].count != i:
                cls.mainLogList[i].count = i + 1
                cls.mainLogList[i].logID = CreateEntry.create_ID(
                                                cls.mainLogList[i].count, 
                                                cls.mainLogList[i].logType, 
                                                cls.mainLogList[i].subtype, 
                                                cls.mainLogList[i].date
                                            )
    # UTILS
    def get_total_entry_count(self) -> int:
        '''Fetches the total count of log Entries in the dynamic main list'''
        return len(Auditing.mainLogList) + 1
    
    def get_current_date(self) -> str:
        return datetime.now().strftime("%d-%m-%Y")

    def get_day(self) -> int:
        try:
            previousDay = Auditing.mainLogList[-1].day
            if self.date != Auditing.mainLogList[-1].date:
                return previousDay + 1
            return previousDay
        except IndexError as e:
            ''' (-) note: should only happen if no Database CSV file was found '''
            return 1
    
    @classmethod
    def check_generic_or_duplicate_titles(cls, title:str) -> str:
        ''' 
        (-) note: Can be improved to only read and set title once instead
                 of reiterating reading & writing of title multiple times
        '''
        def add_title_count(duplicateTitle) -> None:
            '''Adds an increasing number to a duplicate title'''

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
            '''These titles are usually done multiple times throughout the day hence the numbering'''
            title = "{} 1".format(title)

        for entry in cls.currLoglist:
            if entry.title == title and title not in excludedTitles:
                print(f"Duplicate title \'{title}\' found, adding...")
                title =  add_title_count(title)

        return title
    

    @classmethod
    def save_all_entries(cls) -> int:
        FileSaver.save_all_data(cls.mainLogList, DEFAULT_FILE_PATH)
        return 1
    
    @staticmethod
    def display_transactions():
        ExtraDisplays.display_transactions()
    
    @classmethod
    def display_single_entry(cls, entry, show_header=False) -> None:
        if show_header == True:
            '''Used for entry deletion and modification visual confirmation'''
            print(f"{"COUNT":<7} {"DAY":<5} {"DATE":<14} {"LOGTYPE":<9} {"SUBTYPE":<10} {"TITLE":<27} {"AMOUNT":<10} {"LOG ID":<30} {"LIABLE NAME":<15}")
            print(f"{entry.count:<7} {entry.day:<5} {entry.date:<14} {entry.logType:<9} {entry.subtype:<10} {entry.title:<27} {entry.amount:<10} {entry.logID:<30} {entry.liaName:<15}")
        else:
            print(f"{entry.count:<7} {entry.day:<5} {entry.date:<14} {entry.logType:<9} {entry.subtype:<10} {entry.title:<27} {entry.amount:<10} {entry.logID:<30} {entry.liaName:<15}")
                
    @classmethod
    def display_entries(cls, filtered=False, search_parameter=None) -> None:
        max_display_limit = 100
        for entry in cls.mainLogList[-max_display_limit-1:]:
            if not filtered:
                cls.display_single_entry(entry)
            elif search_parameter in entry.logType or search_parameter in entry.subtype:
                cls.display_single_entry(entry)
            elif search_parameter in entry.liaName:
                cls.display_single_entry(entry)
        print(f"{"COUNT":<7} {"DAY":<5} {"DATE":<14} {"LOGTYPE":<9} {"SUBTYPE":<10} {"TITLE":<27} {"AMOUNT":<15} {"LOG ID":<30} {"LIABLE NAME":<15}")

    @classmethod
    def search_entry(cls) -> int:
        ''' Returns index of searched entry based on the main log list '''

        user_input:str = None
        while True:
            # MAIN BROAD SEARCH
            while True:
                print("What log entry to search for?: ")
                print("\tLOGTYPES:     -> (tra/lia/sav)")
                print("\tSUBTYPES: tra -> (debi/cred)")
                print("\t          lia -> (loan/retu/owed/paid)")
                print("\t          sav -> (depo/with)")
                print("\tNAMES:        -> (name)")
                print("\tGo Back:      -> (back)")

                user_input = input("   > ").strip().lower()

                if user_input == "back":
                    return 0
                elif user_input in ["tra","lia","sav"] or \
                    user_input in ["debi","cred","loan","owed","depo","with"] or \
                    user_input in ["name"]:

                    break

                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

            # LIABILITIES NAME SEARCH
            if user_input == "name":
                print("DISPLAY")
                for entry in cls.mainLogList:
                    if entry.liaName != "NON-LIA" and entry.liaName != "NOT_SET":
                        cls.display_single_entry(entry)
                user_input = input("Enter the name to display all logs of: ").strip().title()


            cls.display_entries(filtered=True, search_parameter=user_input)

            # SPECIFIC ENTRY SEARCH
            while True:
                user_input = input("Enter the logID (\'back\' to return): ").strip()

                if user_input == "back":
                    break
                else:
                    for entry in cls.mainLogList:
                        if entry.logID == user_input:
                            return cls.mainLogList.index(entry)
                    print(f"ID of \'{user_input}\' not found")
                    return 0



class ExtraDisplays(Auditing):
    @classmethod
    def display_transactions(cls) -> None:
        print(f"| {"COUNT":<7} | {"DAY":<5} | {"DATE":<14} | {"TITLE":<21} | {"DEBIT":^13} | {"CREDIT":^13} |")
        prevDate = None

        max_display_limit = 100
        for entry in cls.mainLogList[-max_display_limit-1:]:

            if entry.logType == "tra":
                if prevDate != entry.date:
                    '''add linebreaks between new dates'''
                    print(f"{"":-<92}")
                    '''only shows day and date once per new date'''
                    if entry.subtype == "debi":
                        print(f"| {entry.count:<7} | {entry.day:<5} | {entry.date:<14} | {entry.title:<21} | {entry.amount:^13} | {"":^13} |")
                    else:   # credit
                        print(f"| {entry.count:<7} | {entry.day:<5} | {entry.date:<14} | {entry.title:<21} | {"":^13} | {entry.amount:^13} |")
                    prevDate = entry.date
                else:
                    '''no longer shows day and date'''
                    if entry.subtype == "debi":
                        print(f"| {entry.count:<7} | {"":<5} | {"":<14} | {entry.title:<21} | {entry.amount:^13} | {"":^13} |")
                    else:   # credit
                        print(f"| {entry.count:<7} | {"":<5} | {"":<14} | {entry.title:<21} | {"":^13} | {entry.amount:^13} |")

    @classmethod
    def display_liabilities(cls) -> None:
        print(f"| {"COUNT":<7} | {"DAY":<5} | {"DATE":<14} | {"TITLE":<30} | {"DEBIT":^13} | {"CREDIT":^13} |")
        prevDate = None

        max_display_limit = 100
        for entry in cls.mainLogList[-max_display_limit-1:]:

            if entry.logType == "lia":
                if prevDate != entry.date:
                    '''add linebreaks between new dates'''
                    print(f"{"":-<92}")
                    '''only shows day and date once per new date'''
                    if entry.subtype in ["returned", "owed"]:
                        print(f"| {entry.count:<7} | {entry.day:<5} | {entry.date:<14} | {entry.title:<21} | {entry.amount:^13} | {"":^13} |")
                    else:   # loaned, paid
                        print(f"| {entry.count:<7} | {entry.day:<5} | {entry.date:<14} | {entry.title:<21} | {"":^13} | {entry.amount:^13} |")
                    prevDate = entry.date
                else:
                    '''no longer shows day and date'''
                    if entry.subtype in ["returned", "owed"]:
                        print(f"| {entry.count:<7} | {"":<5} | {"":<14} | {entry.title:<21} | {entry.amount:^13} | {"":^13} |")
                    else:   # credit
                        print(f"| {entry.count:<7} | {"":<5} | {"":<14} | {entry.title:<21} | {"":^13} | {entry.amount:^13} |")


class Main:
    def main() -> None:
        audit = Auditing()

        user = None
        status = None

        while user != 0:
            try:
                print("What to do?:")
                print("\t  1. \'Create Entry\'") 
                print("\t  2. \'Modify Entry\'") 
                print("\t  3. \'Delete Entry\'") 
                print("\t  4. \'Use Search Filter\'")
                print("\t  5. \'Display Transactions\'")
                print("\t  6. \'Display all Entries\'") 
                print("\t  7. \'Save all Entries\'") 
                print("\t  0. \'Save and Exit\'") 

                user = int(input("   > ").strip())
            except ValueError as e: print(f"INVALID_INPUT: {e}")

            if   user == 1: # Create an Entry
                status = audit.create_entry()
                if status == 1: print("\n" ," Entry successfully created! ".center(54,"~"), "\n")
                else:           print("\n" ," Entry creation failed... ".center(54,"~"), "\n")

            elif user == 2: # Modify an Entry
                status = audit.modify_entry()
                if status == 1: print("\n" ," Entry successfully modified! ".center(54,"~"), "\n")
                else:           print("\n" ," Entry modification failed... ".center(54,"~"), "\n")

            elif user == 3: # Delete an Entry
                status = audit.delete_entry()
                if status == 1: print("\n" ," Entry successfully deleted! ".center(54,"~"), "\n")
                else:           print("\n" ," Entry deletion failed... ".center(54,"~"), "\n")

            elif user == 4: # Search for specific categories
                status = audit.search_entry()
                if status == 1: print("\n" ," Entry search success! ".center(54,"~"), "\n")
                else:           print("\n" ," Entry search failed... ".center(54,"~"), "\n")

            elif user == 5: # Display all TRANSACTIONS
                audit.display_transactions()

            elif user == 6: # Display ALL Entries
                audit.display_entries()

            elif user == 7: # Save all Entries
                status = audit.save_all_entries()
                print("\n" ," Saved all Entries! ".center(54,"~"), "\n")

        audit.save_all_entries()
        print(f"\'{DEFAULT_FILE_PATH}\' saved successfully".center(100,"~"), "\n")
        print("exiting...")
        del audit
        return






if __name__ == '__main__':
    print("/","".center(50,"-"),"\\")
    print("|","Welcome to Audit Manager v.1".center(50,"-"),"|")
    print("\\","".center(50,"-"),"/")

    Main.main()