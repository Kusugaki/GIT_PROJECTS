from datetime import datetime
from AuditFileHandling import FileGetter, FileSaver
from LogDetails import Transac, Liabili, Savings
# import json
import csv
import os

# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = "AUDIT_LOG.csv"
DEFAULT_FILE_PATH:str = os.path.join(os.getcwd(), DEFAULT_FILE_NAME)

print(DEFAULT_FILE_PATH)



class LogEntry:
    def __init__(self, date:str, logType:str, subtype:str, title:str, amount:float):
        self.date    = date
        self.logType = logType
        self.subtype = subtype
        self.title   = title
        self.amount  = amount

    # def to_dict(self) -> None:
    #     return {
    #         "date":       self.date,
    #         "logType":    self.logType,
    #         "subtype":    self.subtype,
    #         "title":      self.title,
    #         "amount":     self.amount
    #     }    



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
                 totalCount:int=1):
        super().__init__(date, logType, subtype, title, amount)
        self.logID      = logID
        self.totalCount = totalCount

    
    def obj_to_dict(self, fetched_obj) -> dict:
        return {
            "date":       fetched_obj.date,
            "logType":    fetched_obj.logType,
            "subtype":    fetched_obj.subtype,
            "title":      fetched_obj.title,
            "amount":     fetched_obj.amount,
            "logID":      fetched_obj.logID,
            "totalCount": fetched_obj.totalCount
        }
          
    
    def dict_to_obj(self, fetched_dict) -> None:
        # for dict_entry in fetched_dict:
        self.date       = fetched_dict["date"]
        self.logType    = fetched_dict["logType"]
        self.subtype    = fetched_dict["subtype"]
        self.title      = fetched_dict["title"]
        self.amount     = fetched_dict["amount"]
        self.logID      = fetched_dict["logID"]
        self.totalCount = fetched_dict["totalCount"]

        Auditing.get_main_list().append(
            Auditing(self.date, self.logType, self.subtype, self.title, self.amount, self.logID, self.totalCount)
            )



    def temp_save_mainLog(self) -> None:
        if not os.path.exists(DEFAULT_FILE_PATH):
            with open(DEFAULT_FILE_PATH, 'x'):
                pass

        with open(DEFAULT_FILE_PATH, 'a', newline='', encoding="utf-8") as output:
            csv_writer = csv.writer(output)

            for entry in Auditing.get_main_list():
                csv_writer.writerow([self.date, self.logType, self.subtype, self.title, self.amount, self.logID, self.totalCount])


    @classmethod
    def temp_fetch_mainLog(cls) -> None:
        with open(DEFAULT_FILE_NAME, 'r', encoding="utf-8") as input:
            csv_reader = csv.reader(input)

            for entry in csv_reader:
                Auditing.get_main_list().append(cls.dict_to_obj(entry))
                



    def create_entry(self):
        # Auditing.temp_fetch_mainLog()

        def init_fetch_date() -> None:
            self.date = datetime.now().strftime('%d-%m-%Y')

        def init_fetch_entry_details() -> None:
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


            def check_generic_title() -> None:
                genericTitles = [ "Pamasahe", "Found", "Lost", "Deposit", "Withdrawal", "Random Magic Sorcery" ]
                if self.title in genericTitles:
                    add_title_count(self.title)

            def check_title_duplicates() -> None:
                for entry in Auditing.get_main_list():
                    if entry.title == Auditing.get_curr_list():
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
            while self.amount == 0: 
                try: self.amount = abs(float(input("Input Transaction Amount: ")))
                except ValueError as e: print(f"NaN_ERROR: {e}")

        def init_create_ID() -> None:
            self.logID = f"{self.totalCount}//{self.logType}//{self.subtype}//{self.date}"
        

        # FUNCTION CALLS
        init_fetch_date()
        init_fetch_entry_details()
        init_fetch_amount()
        init_create_ID()


        # TEST TEST TEST TEST
        print(f"\n{Auditing.mainLogList = }\n")

        Auditing.mainLogList.append(self)
        Auditing.currLoglist.append(self)

        print(f"\n{Auditing.mainLogList = }\n")

        self.temp_save_mainLog()

        return self
    # END OF CREATE_ENTRY


    def display_entry(self):
        print(f"\n{self.date = }\n{self.logType = }\n{self.subtype = }\n{self.title = }\n{self.amount = }\n{self.logID = }\n")
        return self


    @classmethod
    def get_total_entry_count(cls) -> int:
        return len(cls.mainLogList) + 1

    @classmethod
    def get_main_list(cls) -> list:
        return cls.mainLogList
    
    @classmethod
    def get_curr_list(cls) -> list:
        return cls.currLoglist






if __name__ == '__main__':
    Auditing().display_entry().create_entry().display_entry()