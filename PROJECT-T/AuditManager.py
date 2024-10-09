import os

from copy import deepcopy
from datetime import datetime

from LogEntry_dataclass import LogEntry
from LogTableDisplays   import TableDisplays
from LogFileHandling    import FileGetter, FileSaver
from LogCreateEntry     import CreateEntry, Transac, Liabili, Savings


# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "audit_database.csv"
DEFAULT_FILE_PATH:str = os.path.join(os.path.dirname(__file__), DEFAULT_FILE_NAME)


# AUDIT MANAGER MAIN CLASS
class Auditing(LogEntry):
    mainLogList:list = []
    currLogList:list = []

    def __str__(self) -> str:
        return str(self.count)

    def __init__(self) -> None:
        ''' Program Startup sequence '''
        self.date            = self.get_current_date()
        Auditing.mainLogList = FileGetter.fetch_saved_database(path=DEFAULT_FILE_PATH)
        Auditing.currLogList = FileGetter.fetch_curr_list(dateToday=self.date)

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
        self.title   = CreateEntry.title.title()    # built in string method ".title()"
        self.amount  = CreateEntry.fetch_amount()
        self.logID   = CreateEntry.create_ID(self.count, self.logType, self.subtype, self.date)
        self.liaName = CreateEntry.liaName if self.logType == Liabili.logTypeDetail else "~~~~~~~"

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
        Auditing.currLogList.append(entry)
        FileSaver.save_and_append_data(entry.__dict__, DEFAULT_FILE_PATH)

        return 1

    
    def modify_entry(self) -> int | None:
        ''' (-) note: implementation of this could be / should be improved '''

        print('\n', " Search for an entry to MODIFY ".center(52,'~'), '\n')

        searched_index:int = Auditing.search_entry()
        
        if searched_index == None:
            print("Entry not found. stopping modification process...\n")
            return None
        
        moddedEntry:object = Auditing.mainLogList[searched_index]

        user_input:str = None
        while user_input not in ['A','B','C','D']:
            user_input = input("Choose data to modify:\n\tA. \'LogType\'\n\tB. \'Subtype\'\n\tC. \'Title\'\n\tD. \'Amount\'\n   > ").strip().upper()

            if user_input == 'A':   # Logtype
                CreateEntry.fetch_entry_details()
                moddedEntry.logType = CreateEntry.logType
                moddedEntry.subtype = CreateEntry.subtype
                moddedEntry.liaName = CreateEntry.liaName
                moddedEntry.title   = CreateEntry.title

            elif user_input == 'B':   # Subtype

                if moddedEntry.logType == "tra":
                    moddedEntry.subtype = Transac.get_log_subtype()

                elif moddedEntry.logType == "lia":
                    moddedEntry.subtype = Liabili.get_log_subtype()
                    moddedEntry.liaName = Liabili.get_liable_entity(liable_subtype=moddedEntry.subtype)
                    moddedEntry.title   = Liabili.get_log_title_from_subtype(name=moddedEntry.liaName)
                
                elif moddedEntry.logType == "sav":
                    moddedEntry.subtype = Savings.get_log_subtype()
                    moddedEntry.title   = Savings.get_log_title_from_subtype()
                else:
                    print("\nMODIFYING_SUBTYPE_ERROR\n")

            elif user_input == 'C':   # Title
                if moddedEntry.logType != 'lia':
                    print(f"Previous title: \'{moddedEntry.title}\'\n")
                    moddedEntry.title = input("Input new Entry Title\n   > ").strip()
                else:
                    moddedEntry.liaName = Liabili.get_liable_entity(liable_subtype=moddedEntry.subtype)
                    moddedEntry.title = Liabili.get_log_title_from_subtype(name=moddedEntry.liaName)

            elif user_input == 'D':   # Amount
                print(f"Previous amount: \'{moddedEntry.amount}\'\n")
                moddedEntry.amount = CreateEntry.fetch_amount()
                
            else:
                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

        moddedEntry.title = Auditing.check_generic_or_duplicate_titles(moddedEntry.title).title()
        moddedEntry.logID = CreateEntry.create_ID(moddedEntry.count, moddedEntry.logType, moddedEntry.subtype, moddedEntry.date)

        print("Entry has been modified. Save changes to update the CSV file.")
        Auditing.debug_display_single_entry(moddedEntry, show_header=True)
        return 1


    @classmethod
    def delete_entry(cls) -> int | None:

        print('\n', " Search for an entry to DELETE ".center(52,'!'), '\n')

        searched_index:int = cls.search_entry()

        if searched_index == None:
            print("Entry not found. stopping deletion process...\n")
            return None

        entry_to_be_deleted:object = cls.mainLogList[searched_index]
        
        cls.debug_display_single_entry(entry_to_be_deleted, show_header=True)
        
        if input("Confirm Entry Deletion (\"yes\")\n\t> ").strip().lower() == "yes":
            cls.mainLogList.pop(searched_index)
            print(f"Entry has been succesfully deleted. Save changes to update the CSV file.")
        else:
            print(f"Stopping deletion process...\n")
            return None
        
        cls.fix_entry_count_jumps(loglist=cls.mainLogList, index=searched_index)

        return 1


    @classmethod
    def save_all_entries(cls) -> int:
        FileSaver.save_all_data(cls.mainLogList, DEFAULT_FILE_PATH)
        return 1
    
    @classmethod
    def export_range_of_entries(cls) -> int:
        cls.display_all_entries()
        listOfEntries:list[LogEntry] = deepcopy(cls.get_ranged_list_of_entries())
        custom_file_path:str = FileSaver.get_custom_path(os.path.dirname(__file__))

        cls.fix_entry_count_jumps(loglist=listOfEntries, index=0)
        FileSaver.save_all_data(listOfEntries, custom_file_path)
        print(f"\nExported to \'{custom_file_path}\'")
        return 1
    
    @staticmethod
    def display_transactions() -> None:
        TableDisplays.display_table(logList=Auditing.mainLogList, specifiedLogtype=[Transac.get_log_type()], debitList=["debi"])

    @staticmethod
    def display_liabilities() -> None:
        TableDisplays.display_table(logList=Auditing.mainLogList, specifiedLogtype=[Liabili.get_log_type()], debitList=["retu", "owed"])

    @staticmethod
    def display_savings() -> None:
        TableDisplays.display_table(logList=Auditing.mainLogList, specifiedLogtype=[Savings.get_log_type()], debitList=["depo"])

    @staticmethod
    def display_all_entries() -> None:
        TableDisplays.display_table(logList=Auditing.mainLogList,
                                    specifiedLogtype=[Transac.get_log_type(), 
                                                      Liabili.get_log_type(), 
                                                      Savings.get_log_type()], 
                                    debitList=['debi', 'retu', 'owed', 'with'])
    
    @staticmethod
    def debug_display_single_entry(entry, show_header=False) -> None:
        TableDisplays.debug_display_table_single_entry(entry=entry, show_header=show_header)
                
    @staticmethod
    def debug_display_entries(filtered=False, search_parameter=None) -> None:
        TableDisplays.debug_display_table(logList=Auditing.mainLogList, filtered=filtered, search_parameter=search_parameter)

    @classmethod
    def display_status(cls) -> int:
        '''Gets the totals of all subtypes of each entry and displays them'''
        debiTotal:float = 0.0
        credTotal:float = 0.0
        loanTotal:float = 0.0
        retuTotal:float = 0.0
        owedTotal:float = 0.0
        paidTotal:float = 0.0
        depoTotal:float = 0.0
        withTotal:float = 0.0

        netTotal:float  = 0.0
        netPercent:float= 0.0
        netSavings:float= 0.0
        netDebts:float  = 0.0
        netLoans:float  = 0.0

        cls.display_all_entries()

        # SUMMATION OF LOGS
        for entry in cls.get_ranged_list_of_entries():
            # MAIN LOG STATUS (all logs)
            if entry.subtype in ['debi', 'retu', 'owed', 'with']:
                debiTotal += entry.amount
            else:
                credTotal += entry.amount

            # LIABILITIES LOG STATUS
            if entry.logType == Liabili.get_log_type():
                if   entry.subtype == "loan":
                    loanTotal += entry.amount
                elif entry.subtype == "retu":
                    retuTotal += entry.amount
                elif entry.subtype == "owed":
                    owedTotal += entry.amount
                elif entry.subtype == "paid":
                    paidTotal += entry.amount

            # SAVINGS LOG STATUS
            if entry.logType == Savings.get_log_type():
                if   entry.subtype == "depo":
                    depoTotal += entry.amount                
                elif entry.subtype == "with":
                    withTotal += entry.amount

        # CALCULATIONS
        netTotal   = debiTotal - credTotal
        
        if debiTotal != 0:
            netPercent = netTotal / debiTotal   # not yet multiplied by 100
        
        netSavings = depoTotal - withTotal
        netDebts   = owedTotal - paidTotal
        netLoans   = loanTotal - retuTotal

        TableDisplays.display_status_table(
                debiTotal, 
                credTotal, 
                loanTotal, 
                retuTotal, 
                owedTotal, 
                paidTotal, 
                depoTotal, 
                withTotal, 
                netTotal, 
                netPercent, 
                netLoans, 
                netDebts, 
                netSavings
            )

        return 1


    @classmethod
    def search_entry(cls) -> int | None:
        ''' Returns index of searched entry based on the main log list, returns None if none was found'''

        user_input:str = None
        while True:
            # MAIN BROAD SEARCH
            while True:
                print("What log entry to search for?: ")
                print("\t   LOGTYPES:    SUBTYPES:")
                print("\t         (tra)  -> (debi/cred)")
                print("\t         (lia)  -> (loan/retu/owed/paid)")
                print("\t         (sav)  -> (depo/with)")
                print("\tNAMES:   (name) ")
                print("\tGo Back: (back) ")

                user_input = input("   > ").strip().lower()

                if user_input == "back":
                    return None
                elif user_input in ["tra","lia","sav"] or \
                    user_input in ["debi","cred","loan", "retu", "owed", "paid","depo","with"] or \
                    user_input in ["name"]:
                    break

                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

            # LIABILITIES NAME SEARCH
            if user_input == "name":
                print("DISPLAY")
                for entry in cls.mainLogList:
                    if entry.liaName != "~~~~~~~" and entry.liaName != "NON-LIA" and entry.liaName != "NOT_SET":
                        ''' (-) note: REMOVE FROM FINAL BUILD: "NON-LIA" and "NOT_SET" are placeholder values'''
                        cls.debug_display_single_entry(entry)
                user_input = input("Enter the name to display all logs of: ").strip().title()

            # SHOW FILTERED ENTRIES
            cls.debug_display_entries(filtered=True, search_parameter=user_input)

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
                    return None

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
        
    @staticmethod
    def fix_entry_count_jumps(loglist:list[LogEntry], index:int):
        for i in range(index, len(loglist)):
            entry = loglist[i]
            if entry.count != i:
                entry.count = i + 1
                entry.logID = CreateEntry.create_ID(
                                                entry.count, 
                                                entry.logType, 
                                                entry.subtype, 
                                                entry.date
                                            )
    
    @classmethod
    def check_generic_or_duplicate_titles(cls, title:str) -> str:
        ''' 
        (-) note: Can be improved to only read and set title once instead
                 of reiterating reading & writing of title multiple times
        '''
        def add_title_count(duplicateTitle) -> str:
            '''Adds an increasing number to a duplicate title'''

            if " " in duplicateTitle:
                parts = duplicateTitle.split(" ")
                try:
                    parts[-1] = str(int(parts[-1]) + 1)
                except ValueError or BaseException as e:
                    print(f"TITLE_ADDITION_ERROR: {e}")
                finally: 
                    return " ".join(parts)
            else:
                return "{} 2".format(duplicateTitle)


        genericTitles = [ "Pamasahe", "Lost", "Found", "Random Magic Sorcery" ]
        excludedTitles= [ "Loaned", "Owed" ]

        if title in genericTitles and not " " in title:
            '''These titles are usually done multiple times throughout the day hence the numbering'''
            title = "{} 1".format(title)

        for entry in cls.currLogList:
            if entry.title == title and title not in excludedTitles:
                print(f"Duplicate title \'{title}\' found, adding...")
                title = add_title_count(title)
        return title
    
    @classmethod
    def get_ranged_list_of_entries(cls) -> list[LogEntry]:
        ''' 
        Returns beginning and ending indexes within a specified range of dates inputted

        (-) note: inefficient 2 pointer approach instead of directly comparing date values (Worst Case: 3n)
            \nThis is an absolute abomination, this whole method is.
        '''
        startDate:str   = None
        endDate:str     = None

        startPtr:int    = 0
        endPtr:int      = startPtr
        logSize:int     = len(cls.mainLogList)

        startDate = input("Choose start date (##-##-####/today) (\'leave blank for first date\')\n\t> ").replace(' ', '').lower()

        if startDate != "today":
            endDate = input("Choose end date (##-##-####/today) (\'leave blank for same date\')\n\t> ").replace(' ', '').lower()
            if startDate == '':
                startDate = cls.mainLogList[0].date
        else:
            startDate = cls.mainLogList[-1].date
            endDate = startDate

        if endDate == "today":
            endDate = cls.mainLogList[-1].date
        elif endDate == '':
            endDate = startDate


        for i in range(logSize):
            if cls.mainLogList[i].date == startDate:
                startPtr = i
                break

        for i in range(startPtr, logSize):
            try:
                if cls.mainLogList[i].date == endDate and \
                (i == logSize-1 or cls.mainLogList[i+1].date != endDate):
                    endPtr = i
                    break
            except IndexError as e:
                print("INDEX_ERROR:", i, e)

        print("\n", " Displaying Entries Status ".center(52,'~'), '\n')

        print(f"Starting on: {cls.mainLogList[startPtr].date} - no. {startPtr+1}")
        print(f"Ending on:   {cls.mainLogList[endPtr].date} - no. {endPtr+1}\n")

        return cls.mainLogList[startPtr:endPtr+1]



if __name__ == "__main__":
    print("YOU ARE RUNNING THE AUDITMANAGER.PY FILE")