from datetime import datetime
from AuditFileHandling import FileGetter, FileSaver
from SubMetadata import Transac, Liabili, Savings
import csv
import os

# GLOBAL VARIABLES
default_file_name:str = "AUDIT_LOG.csv"
default_file_path:str = os.path.join(os.getcwd(), default_file_name)



class LogEntry:
    def __init__(self, date:str, logType:str, subtype:str, title:str, amount:float):
        self.date    = date
        self.logType = logType
        self.subtype = subtype
        self.title   = title
        self.amount  = amount

    def to_dict(self) -> None:
        return {
            "date":       self.date,
            "logType":    self.logType,
            "subtype":    self.subtype,
            "title":      self.title,
            "amount":     self.amount
        }    

# MAIN CLASS - OVERHAULED
class Auditing(LogEntry):
    mainLogList:list = []
    currLoglist:list = []

    def __init__(self, 
                 date:str=None, 
                 logType:str=None,
                 subtype:str=None,
                 title:str=None, 
                 amount:float=0, 
                 logID:str=None, 
                 totalCount:int=0):
        super().__init__(date, logType, subtype, title, amount, logID, totalCount)
        self.logID      = logID
        self.totalCount = totalCount

    def create_entry(self):
        def init_date_handling():
            self.date = datetime.now().strftime('%Y-%m-%d')

        def init_fetch_entry_details():
            ''' Fetches info for LOGTYPE, Log SUBTYPE, and TITLE '''

            def add_title_count(duplicateTitle) -> None:
                ''' Adds an increasing number to a duplicate/generic title '''

                if " " in duplicateTitle:
                    duplicateTitle = duplicateTitle.split(" ")
                    try:
                        duplicateTitle[-1] = str(int(duplicateTitle[-1]) + 1)
                    except ValueError or BaseException as e:
                        print(f"TITLE_ADDITION_ERROR:\n\t{e}")
                    finally: 
                        self.title = " ".join(duplicateTitle)
                else:
                    self.title = "{} 1".format(duplicateTitle)

            def check_generic_title():
                genericTitles = [ "Pamasahe", "Found", "Lost", "Deposit", "Withdrawal", "Random Magic Sorcery" ]
                if self.title in genericTitles:
                    add_title_count(self.title)

            def check_title_duplicates():
                for entry in Auditing.get_main_list():
                    if entry.title == Auditing.get_curr_list():
                        print(f"Duplicate title \'{self.title}\' found, adding...")
                        add_title_count(self.title)


            # Main Function
            user_input = None

            while user_input not in ['A','B','C']:
                user_input = input("""Enter Log Type:\n\tA. \'Transactions\'\n\tB. \'Liabilities\'\n\tC. \'Savings\'\n  > """).upper()

                match user_input:
                    case 'A':
                        Transac.fetch_metadata_details()
                        self.logType = Transac.logType
                        self.subtype = Transac.subtype
                        self.title   = input("Input Log Title: ")
                    case 'B':
                        Liabili.fetch_metadata_details()
                        self.logType = Liabili.logType
                        self.subtype = Liabili.subtype
                        self.title   = Liabili.titleChoice
                    case 'C':
                        Savings.fetch_metadata_details()
                        self.logType = Savings.logType
                        self.subtype = Savings.subtype
                        self.title   = Savings.titleChoice
                    case _:
                        print(f"ERROR: \'{user_input}\' is not part of the options.\n")
                        continue

                check_generic_title()
                check_title_duplicates()

        def init_fetch_amount():
            while self.amount == 0: 
                try: self.amount = abs(float(input("Input Transaction Amount: ")))
                except ValueError as e: print(f"NaN_ERROR: {e}")

        def init_ID():
            return f"{self.totalCount}//{self.logType}//{self.subtype}//{self.date}"
        

        # FUNCTION CALLS
        init_date_handling()
        init_fetch_entry_details()
        init_fetch_amount()
        init_ID()

        Auditing.mainLogList.append(self)
        Auditing.currLoglist.append(self)

    


    @classmethod
    def get_main_list(cls):
        return cls.mainLogList
    
    @classmethod
    def get_curr_list(cls):
        return cls.currLoglist






if __name__ == '__main__':
    print(os.path.join(os.getcwd(), "AUDIT_LOG.csv"))

    Auditing().fetch_metadata()