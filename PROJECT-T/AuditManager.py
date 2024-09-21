import os
import time

from datetime import datetime

from LogFileHandling import FileGetter, FileSaver
from LogEntry_dataclass import LogEntry
from LogCreateEntry import Transac, Liabili, Savings
from LogCreateEntry import CreateEntry


# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "audit_database.csv"
DEFAULT_FILE_PATH:str = os.path.join(os.path.dirname(__file__), DEFAULT_FILE_NAME)
MAX_DISPLAY_LIMIT:int = 100


# AUDIT MANAGER MAIN CLASS
class Auditing(LogEntry):
    mainLogList:list = []
    currLoglist:list = []

    def __str__(self) -> str:
        return str(self.count)

    def __init__(self) -> None:
        ''' Program Startup sequence '''
        self.date = datetime.now().strftime("%d-%m-%Y")
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
        Auditing.currLoglist.append(entry)
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

                if moddedEntry.logType == Liabili.logTypeDetail:
                    moddedEntry.liaName = Liabili.get_liable_entity(liable_subtype=moddedEntry.subtype)
                    moddedEntry.title   = Liabili.get_log_title_from_subtype(name=moddedEntry.liaName)
                else:
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
                print(f"Previous title: \'{moddedEntry.title}\'\n")
                moddedEntry.title = input("Input new Entry Title\n   > ").strip()

            elif user_input == 'D':   # Amount
                print(f"Previous amount: \'{moddedEntry.amount}\'\n")
                moddedEntry.amount = CreateEntry.fetch_amount()
                
            else:
                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

        moddedEntry.title = Auditing.check_generic_or_duplicate_titles(moddedEntry.title)
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
        
        '''Fixing entry count jumps'''
        for i in range(searched_index, len(cls.mainLogList)):
            if cls.mainLogList[i].count != i:
                cls.mainLogList[i].count = i + 1
                cls.mainLogList[i].logID = CreateEntry.create_ID(
                                                cls.mainLogList[i].count, 
                                                cls.mainLogList[i].logType, 
                                                cls.mainLogList[i].subtype, 
                                                cls.mainLogList[i].date
                                            )
        return 1


    @classmethod
    def save_all_entries(cls) -> int:
        FileSaver.save_all_data(cls.mainLogList, DEFAULT_FILE_PATH)
        return 1
    
    @staticmethod
    def display_transactions() -> None:
        TableDisplays.display_table(specifiedLogtype=[Transac.get_log_type()], debitList=["debi"])

    @staticmethod
    def display_liabilities() -> None:
        TableDisplays.display_table(specifiedLogtype=[Liabili.get_log_type()], debitList=["retu", "owed"])

    @staticmethod
    def display_savings() -> None:
        TableDisplays.display_table(specifiedLogtype=[Savings.get_log_type()], debitList=["depo"])

    @staticmethod
    def display_all_entries() -> None:
        TableDisplays.display_table(specifiedLogtype=[Transac.get_log_type(), 
                                                      Liabili.get_log_type(), 
                                                      Savings.get_log_type()], 
                                    debitList=['debi', 'retu', 'owed', 'with'])
    
    @staticmethod
    def debug_display_single_entry(entry, show_header=False) -> None:
        TableDisplays.debug_display_table_single_entry(entry=entry, show_header=show_header)
                
    @staticmethod
    def debug_display_entries(filtered=False, search_parameter=None) -> None:
        TableDisplays.debug_display_table(filtered=filtered, search_parameter=search_parameter)


    def display_status(self) -> int:
        '''Gets the totals of all subtypes of each entry and displays them'''
        '''This is an absolute abomination, this whole method is.'''
        debiTotal:float = 0.0
        credTotal:float = 0.0
        loanTotal:float = 0.0
        retuTotal:float = 0.0
        owedTotal:float = 0.0
        paidTotal:float = 0.0
        depoTotal:float = 0.0
        withTotal:float = 0.0

        startDate:str
        endDate:str


        TableDisplays.display_all_entries()

        startDate = input("Choose start date\n\t> ")
        endDate = input("Choose end date (leave blank for same date)\n\t> ")

        if endDate == '':
            endDate = startDate

        startPtr:int = 0
        endPtr:int = 0
        endPtrDateFound = False
        logSize:int = len(Auditing.mainLogList)

        ''' 
        (-) note: inefficient 2 pointer approach instead of directly comparing date values (Worst Case: 3n)
        (-) note: Put this 2 pointer search in its own method so that other methods can use it too
        '''
        for i in range(logSize):
            if Auditing.mainLogList[i].date == startDate:
                startPtr = i
                break
        for i in range(startPtr, logSize):
            try:
                if endPtrDateFound:
                    if i == logSize-1 or Auditing.mainLogList[i+1].date != endDate:
                        endPtr = i
                        break
                elif Auditing.mainLogList[i].date == endDate:
                    endPtrDateFound = True
            except IndexError as e:
                print("INDEX_ERROR:", i, e)

        print("\n", " Displaying Entries Status ".center(52,'~'), '\n')

        print(f"Starting on: {Auditing.mainLogList[startPtr].date} - no. {startPtr+1}")
        print(f"Ending on:   {Auditing.mainLogList[endPtr].date} - no. {endPtr+1}")

        for i in range(startPtr, endPtr+1):
            entry = Auditing.mainLogList[i]

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


        netTotal   = debiTotal - credTotal
        loanTotal  = loanTotal - retuTotal
        owedTotal  = owedTotal - paidTotal
        netSavings = depoTotal - withTotal

        TableDisplays.display_status_table(netTotal=netTotal, loans=loanTotal, owed=owedTotal, savings=netSavings)

        return 1


    @classmethod
    def search_entry(cls) -> int | None:
        ''' Returns index of searched entry based on the main log list, returns None if none was found'''

        user_input:str = None
        while True:
            # MAIN BROAD SEARCH
            while True:
                print("What log entry to search for?: ")
                print("\tLOGTYPES:      SUBTYPES:")
                print("\t      (tra) -> (debi/cred)")
                print("\t      (lia) -> (loan/retu/owed/paid)")
                print("\t      (sav) -> (depo/with)")
                print("\tNAMES:      -> (name)")
                print("\tGo Back:    -> (back)")

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

        for entry in cls.currLoglist:
            if entry.title == title and title not in excludedTitles:
                print(f"Duplicate title \'{title}\' found, adding...")
                title = add_title_count(title)
        return title
    





class TableDisplays(Auditing):
    '''Table column width "percentages" '''
    percount   = 5
    perday     = 3
    perdate    = 12
    perlogtype = 7
    persubtype = 7
    pertitle   = 25
    peramount  = 13
    perID      = 30
    perliaName = 15

    perdebit   = 13
    percredit  = 12

    @classmethod
    def display_table(cls, specifiedLogtype:list[str], debitList:list[str]) -> None:
        perTotal = cls.percount + cls.perday + cls.perdate + cls.pertitle + cls.perdebit + cls.percredit + 17 # accounting for table vertical line spacings
        prevDate = None

        '''Show header'''
        print(f" {"":_<{perTotal}}")
        print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"TITLE":^{cls.pertitle}} | {"DEBIT":^{cls.perdebit}} | {"CREDIT":^{cls.percredit}} |")
        for entry in cls.mainLogList[-MAX_DISPLAY_LIMIT-1:]:

            if entry.logType in specifiedLogtype:

                if prevDate != entry.date:
                    '''add linebreaks between new dates'''
                    print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.perdebit}}-|-{"":-<{cls.percredit}}-|")
                    '''only shows day and date once per new date'''
                    if entry.subtype in debitList:
                        print(f"| {entry.count:<{cls.percount}} | {entry.day:^{cls.perday}} | {entry.date:^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {entry.amount:^{cls.perdebit}} | {"":^{cls.percredit}} |")
                    else:   # loaned, paid
                        print(f"| {entry.count:<{cls.percount}} | {entry.day:^{cls.perday}} | {entry.date:^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {"":^{cls.perdebit}} | {entry.amount:^{cls.percredit}} |")
                    prevDate = entry.date
                else:
                    '''no longer shows day and date'''
                    if entry.subtype in debitList:
                        print(f"| {entry.count:<{cls.percount}} | {"":^{cls.perday}} | {"":^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {entry.amount:^{cls.perdebit}} | {"":^{cls.percredit}} |")
                    else:   # credit
                        print(f"| {entry.count:<{cls.percount}} | {"":^{cls.perday}} | {"":^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {"":^{cls.perdebit}} | {entry.amount:^{cls.percredit}} |")
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.perdebit}}-|-{"":-<{cls.percredit}}-|")
        print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"TITLE":^{cls.pertitle}} | {"DEBIT":^{cls.perdebit}} | {"CREDIT":^{cls.percredit}} |")
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.perdebit}}-|-{"":-<{cls.percredit}}-|")
    
    @classmethod
    def display_status_table(cls, netTotal, loans, owed, savings):
        amountWidth = cls.peramount + 4
        print(f" {"":_<{cls.pertitle + amountWidth + 5}}")
        print(f"| {"TOTALS":^{cls.pertitle}} | {"AMOUNT":^{amountWidth}} |")
        print(f"|-{"":-<{cls.pertitle}}-|-{"":-<{amountWidth}}-|")
        print(f"| {"Net Total":<{cls.pertitle}} | {netTotal:^{amountWidth}} |")
        print(f"|-{"":-<{cls.pertitle}}-|-{"":-<{amountWidth}}-|")
        print(f"| {"Loaned Amount":<{cls.pertitle}} | {loans:^{amountWidth}} |")
        print(f"| {"Owed Amount":<{cls.pertitle}} | {owed:^{amountWidth}} |")
        print(f"|-{"":-<{cls.pertitle}}-|-{"":-<{amountWidth}}-|")
        print(f"| {"Current Savings":<{cls.pertitle}} | {savings:^{amountWidth}} |")
        print(f"|-{"":-<{cls.pertitle}}-|-{"":-<{amountWidth}}-|")


    @classmethod
    def debug_display_table(cls, filtered=False, search_parameter=None) -> None:
        perTotal = cls.percount + cls.perday + cls.perdate + cls.perlogtype + cls.persubtype + cls.pertitle + cls.peramount + cls.perID + cls.perliaName + 27 # accounting for table vertical line spacings

        print(f" {"":_<{perTotal-1}}")
        
        for entry in cls.mainLogList[-MAX_DISPLAY_LIMIT-1:]:
            if not filtered:
                cls.debug_display_table_single_entry(entry)
            elif search_parameter in entry.logType or search_parameter in entry.subtype:
                cls.debug_display_table_single_entry(entry)
                                                                        # (-) note: REMOVE THESE PLACEHOLDER LIABILITY NAMES
            elif search_parameter in entry.liaName and entry.liaName != "~~~~~~~" and entry.liaName != "NON-LIA" and entry.liaName != "NOT_SET":
                cls.debug_display_table_single_entry(entry)

        '''Show footer details'''
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")
        print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"LOGTYPE":^{cls.perlogtype}} | {"SUBTYPE":^{cls.persubtype}} | {"TITLE":^{cls.pertitle}} | {"AMOUNT":^{cls.peramount}} | {"LOG ID":^{cls.perID}} | {"LIABLE NAME":^{cls.perliaName}} |")
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")

    @classmethod
    def debug_display_table_single_entry(cls, entry, show_header=False) -> None:
        if show_header == False:
            '''Used for displaying whole table'''
            print(f"| {entry.count:<{cls.percount}} | {entry.day:<{cls.perday}} | {entry.date:<{cls.perdate}} | {entry.logType:<{cls.perlogtype}} | {entry.subtype:<{cls.persubtype}} | {entry.title:<{cls.pertitle}} | {entry.amount:<{cls.peramount}} | {entry.logID:<{cls.perID}} | {entry.liaName:<{cls.perliaName}} |")
        else:
            '''Used for entry deletion and modification visual confirmation'''
            print(f" {"":_<{cls.percount + cls.perday + cls.perdate + cls.perlogtype + cls.persubtype + cls.pertitle + cls.peramount + cls.perID + cls.perliaName + 26}}")
            print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"LOGTYPE":^{cls.perlogtype}} | {"SUBTYPE":^{cls.persubtype}} | {"TITLE":^{cls.pertitle}} | {"AMOUNT":^{cls.peramount}} | {"LOG ID":^{cls.perID}} | {"LIABLE NAME":^{cls.perliaName}} |")
            print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")
            print(f"| {entry.count:<{cls.percount}} | {entry.day:<{cls.perday}} | {entry.date:<{cls.perdate}} | {entry.logType:<{cls.perlogtype}} | {entry.subtype:<{cls.persubtype}} | {entry.title:<{cls.pertitle}} | {entry.amount:<{cls.peramount}} | {entry.logID:<{cls.perID}} | {entry.liaName:<{cls.perliaName}} |")
            print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")
    
            # print("|-{0:<{1}}-|-{1:<{cls.perday}}-|-{2:<{cls.perdate}}-|-{3:<{cls.perlogtype}}-|-{4:<{cls.persubtype}}-|-{5:<{cls.pertitle}}-|-{6:<{cls.peramount},f}-|-{7:<{cls.perID}}-|-{8:<{cls.perliaName}}-|".format("", "", "", "", "", "", "", "", ""))
            # print("| {0:<{1}} | {1:<{cls.perday}} | {2:<{cls.perdate}} | {3:<{cls.perlogtype}} | {4:<{cls.persubtype}} | {5:<{cls.pertitle}} | {6:<{cls.peramount},f} | {7:<{cls.perID}} | {8:<{cls.perliaName}} |".format(entry.count, entry.day, entry.date, entry.logType, entry.subtype, entry.title, entry.amount, entry.logID, entry.liaName))
            # print("|-{0:<{1}}-|-{1:<{cls.perday}}-|-{2:<{cls.perdate}}-|-{3:<{cls.perlogtype}}-|-{4:<{cls.persubtype}}-|-{5:<{cls.pertitle}}-|-{6:<{cls.peramount},f}-|-{7:<{cls.perID}}-|-{8:<{cls.perliaName}}-|".format("", "", "", "", "", "", "", "", ""))

if __name__ == "__main__":
    print("YOU ARE RUNNING THE AUDITMANAGER.PY FILE")