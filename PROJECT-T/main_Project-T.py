# Functions & Definitions
# 1. Program automatically updates important changes at startup
# 2. Automatically determine the date and create a new log once it changes
# 3. At the end of the day, display out the main compiled auditTrail of all logTypes as one
# 4. Create attributes for Debit:Credit, Deposit:Withdrawals, and Loaned:Debt
# 5. All changes in the logs shall automatically be inputted into the Audit Trail
# 6. A list of methods shall be:
#       a.) New Transaction (with parameter of logType)
#       b.) Delete Transaction
#       c.) Modify Log
#       d.) Display Log (with parameter of logType)
#       e.) Display Audit Trail (logs compiler)
#       f.) Search Logs (using date, day, logType, etc.)
# 7. All final changes shall be saved to a .json or .csv file
# 8. A list of important attributes shall be:
#       a.) day
#       b.) date
#       c.) title (log Title)
#       d.) amount
#       e.) logType (transac/savings/lendings)
#       f.) logID (identifiers for specific logs to modify)
#           i.) FORMAT ==> %day-%index-%logType (example: 02-253-sav)
#       g.) logCount (total amount of logs created in the main Audit Trail)
#           i.) possibly add a checkpoint/achievement system for every "count % 100" logs

from datetime import datetime
from AuditFileHandling import FileGetter, FileSaver
from SubMetadata import Transac, Liabili, Savings
import csv
import os


class Log_Entry:
    def __init__(self, date, title, amount, logType, subtype, logID, logCount=0, day=0):
        self.date     = date
        self.logType  = logType
        self.subtype  = subtype
        self.title    = title
        self.amount   = amount
        self.logID    = logID
        self.logCount = logCount
        self.day      = day

    def to_dict(self) -> None:
        return {
            "logCount": self.logCount,
            "day":      self.day,
            "date":     self.date,
            "logType":  self.logType,
            "subtype":  self.subtype,
            "title":    self.title,
            "amount":   self.amount,
            "logID":    self.logID
        }    


# MAIN CLASS
class Auditing:
    default_audit_name = "AUDIT_LOG.csv"
    default_audit_path = os.path.join(os.getcwd(), default_audit_name)
    audit_file_path    = ""
    logList            = []
    currentDateLogList = []
    logCount           = len(logList) # PLACEHOLDER VALUE
    currentDate        = datetime.now().strftime('%Y-%m-%d')

    @classmethod
    def audit_startup(cls):
        cls.audit_file_path = FileGetter.get_path(cls.default_audit_path)

        cls.logList = FileGetter.get_main_log()

        if cls.has_date_changed():
            FileSaver.save_previous_entries(cls.audit_file_path)
        # and other potential startup methods

    @classmethod
    def has_date_changed(cls) -> bool:
        return cls.currentDate == cls.logList[-1].date 
    

    @classmethod
    def get_current_date_log_list(cls):
        return cls.currentDateLogList


    # DETERMINE TRANSACTION LOCATION FOR DEBIT CREDIT BY ASSIGNING THE AMOUNT WITH NEGATIVE OR POSITIVE NUMBERS
    # ADD has_date_changed() LOGIC TO THIS PRIOR TO ENTRY CREATION
    @classmethod    # class methods do not involve the specific instances whatsoever
    def create_new_entry(cls):
        cls.__logSubType :str   = None
        cls.__logType    :str   = None
        cls.__title      :str   = None
        cls.__logID      :str   = None
        cls.__amount     :float = None
        
        cls.determine_entry_metadata()
        cls.check_generic_title()
        cls.check_title_duplicates()
        cls.create_log_ID()

        while cls.__amount is None: 
            try: cls.__amount = abs(float(input("Input Transaction Amount: ")))
            except ValueError as e: print(f"NaN_ERROR: {e}")


        # TEST TEST TEST TEST REMOVE THESE CODE BLOCKS
        print(f"\n{cls.currentDate  = }\n{cls.__logType    = }\n{cls.__logSubType = }\n{cls.__title      = }\n{cls.__amount     = }\n")

        print(f"log ID format: \'LogCount\'+\'LogType\'+\'Subtype\'+\'Date\'")
        print(f"{cls.__logID = }\n")

        print(f"{cls.default_audit_path = }")



    @classmethod
    def determine_entry_metadata(cls) -> None:
        logTypeOptions = ['A','B','C']

        for i in range(5):
            logTypeChoice = input("""Enter Log Type:\n\tA. \'Transactions\'\n\tB. \'Liabilities\'\n\tC. \'Savings\'\n  > """).upper()
            
            try: 
                assert logTypeChoice in logTypeOptions 
                break
            except AssertionError: print(f"ASSERTION_ERROR: \'{logTypeChoice}\' is not in the Options.\n")
        else:
            print("FAILED TO INPUT LOG TYPE\n") 

        match logTypeChoice:
            case 'A' | 'a':
                Transac.fetch_metadata_details()
                cls.__logType    = Transac.logType
                cls.__logSubType = Transac.subtype
                cls.__title      = input("Input Log Title: ")
            case 'B' | 'b':
                Liabili.fetch_metadata_details()
                cls.__logType    = Liabili.logType
                cls.__logSubType = Liabili.subtype
                cls.__title      = Liabili.titleChoice
            case 'C' | 'c':
                Savings.fetch_metadata_details()
                cls.__logType    = Savings.logType
                cls.__logSubType = Savings.subtype
                cls.__title      = Savings.titleChoice
            case _:
                print("LOG_SELECTION_ERROR: DEFAULTING TO \'TRANSACTION\' LOG_TYPE")
                Transac.fetch_metadata_details()
                cls.__logType    = Transac.logType
                cls.__logSubType = Transac.subtype

    @classmethod
    def check_generic_title(cls) -> FileNotFoundError:
        genericTitles = [ "Pamasahe", "Found", "Lost", "Deposit", "Withdrawal", "Random Magic Sorcery" ]
        if cls.__title in genericTitles:
            cls.add_title_count(cls.__title)

    @classmethod
    def check_title_duplicates(cls):
        for entry in cls.currentDateLogList:
            if cls.__title == cls.currentDateLogList.title:
                print(f"Duplicate title \'{cls.__title}\' found, adding...")
                cls.add_title_count(cls.__title)

    @classmethod
    def add_title_count(cls, newTitle) -> None:
        if " " in newTitle:
            newTitle = newTitle.split(" ")
            try:
                newTitle[-1] = str(int(newTitle[-1]) + 1)
            except ValueError or BaseException as e:
                print(f"TITLE_ADDITION_ERROR:\n\t{e}")
            finally: 
                cls.__title = " ".join(newTitle)
        else:
            cls.__title = "{} 1".format(newTitle)

    @classmethod
    def create_log_ID(cls):
        cls.__logID = f"{cls.logCount}//{cls.__logType}//{cls.__logSubType}//{cls.currentDate}"





if __name__ == '__main__':
    print(os.path.join(os.getcwd(), "AUDIT_LOG.csv"))

    Auditing.create_new_entry()