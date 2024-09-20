from abc import ABC, abstractmethod


class CreateEntry:
    logType:str = "CREATE_ENTRY_DEFAULT"
    subtype:str = "CREATE_ENTRY_DEFAULT"
    title:str   = "CREATE_ENTRY_DEFAULT"
    liaName:str = "CREATE_ENTRY_DEFAULT"

    @classmethod
    def fetch_entry_details(cls) -> None:
        '''Fetches info for LOGTYPE, Log SUBTYPE, and TITLE'''

        user_input = None
        while user_input not in ['A','B','C']:
            user_input = input("""Enter Log Type:\n\tA. \'Transactions\'\n\tB. \'Liabilities\'\n\tC. \'Savings\'\n  > """).strip().upper()

            if   user_input == 'A': # Transactions
                cls.logType = Transac.get_log_type()
                cls.subtype = Transac.get_log_subtype()
                cls.title   = Transac.get_log_title_from_subtype()
            elif user_input == 'B': # Liabilities
                cls.logType = Liabili.get_log_type()
                cls.subtype = Liabili.get_log_subtype()
                cls.liaName = Liabili.get_liable_entity(cls.subtype)
                cls.title   = Liabili.get_log_title_from_subtype(cls.liaName)
            elif user_input =='C':  # Savings
                cls.logType = Savings.get_log_type()
                cls.subtype = Savings.get_log_subtype()
                cls.title   = Savings.get_log_title_from_subtype()
            else:
                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

    @staticmethod
    def fetch_amount() -> float:
        while True:
            try: return abs(float(input("Input Transaction Amount: ").strip()))
            except ValueError as e: print(f"NaN_ERROR: {e}")

    @staticmethod
    def create_ID(count, logType, subtype, date) -> str:
        '''Creates a unique ID'''
        return f"{count}//{logType}//{subtype}//{date}"
    




# ABSTRACT CLASS
class LogDetails(ABC):
    logTypeDetail:       str
    subtypeChoiceDetail: list[str] # peaniths
    logTitleDetail:      str

    @classmethod
    def get_log_type(cls) -> str:
        return cls.logTypeDetail
        # return cls.logTypeDetail[:3].lower()  # previously for "Transactions", "Liabilities", "Savings" LogTypeFulltitles
    
    @classmethod
    def get_log_subtype(cls) -> str:
        user_input:str = None
        while user_input not in ['A','B']:
            user_input = input(f"Enter subtype:\n\tA. \'{cls.subtypeChoiceDetail[0]}\'\n\tB. \'{cls.subtypeChoiceDetail[1]}\'\n  > ").strip().upper()

            if   user_input == 'A':
                cls.logTitleDetail = cls.subtypeChoiceDetail[0]
                return cls.subtypeChoiceDetail[0][:4].lower()
            elif user_input == 'B':
                cls.logTitleDetail = cls.subtypeChoiceDetail[1]
                return cls.subtypeChoiceDetail[1][:4].lower()
            else:
                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

    @classmethod
    @abstractmethod
    def get_log_title_from_subtype(cls) -> str:
        return cls.logTitleDetail





class Transac(LogDetails):
    logTypeDetail = "tra" # "Transactions"
    subtypeChoiceDetail = ["Debit", "Credit"]

    def get_log_title_from_subtype() -> str:
        return input("Input Entry Title: ").strip()


class Liabili(LogDetails):
    logTypeDetail = "lia" # "Liabilities"
    subtypeChoiceDetail = ["Loaned", "Returned", "Owed", "Paid"]
        
    @classmethod
    def get_log_subtype(cls) -> str:
        user_input:str = None
        while user_input not in ['A','B','C','D']:
            user_input = input(f"Enter liability type:\n\tA. \'{cls.subtypeChoiceDetail[0]}\'\n\tB. \'{cls.subtypeChoiceDetail[1]}\'\n\tC. \'{cls.subtypeChoiceDetail[2]}\'\n\tD. \'{cls.subtypeChoiceDetail[3]}\'\n   > ").strip().upper()

            if   user_input == 'A':   # Loaned
                cls.logTitleDetail = cls.subtypeChoiceDetail[0]
                return cls.subtypeChoiceDetail[0][:4].lower()
            
            elif user_input == 'B':   # Returned
                cls.logTitleDetail = cls.subtypeChoiceDetail[1]
                return cls.subtypeChoiceDetail[1][:4].lower()
            
            elif user_input == 'C':   # Owed
                cls.logTitleDetail = cls.subtypeChoiceDetail[2]
                return cls.subtypeChoiceDetail[2][:4].lower()
            
            elif user_input == 'D':   # Paid
                cls.logTitleDetail = cls.subtypeChoiceDetail[3]
                return cls.subtypeChoiceDetail[3][:4].lower()
            
            else:
                print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

    @classmethod
    def get_log_title_from_subtype(cls, name) -> str:
        return f"{cls.logTitleDetail:<9}-> ({name})"

    @staticmethod
    def get_liable_entity(liable_subtype) -> str:
        if   liable_subtype == Liabili.subtypeChoiceDetail[0][:4].lower(): # Loaned
            return input("Loaned to whom?: ").strip().title()
        elif liable_subtype == Liabili.subtypeChoiceDetail[1][:4].lower(): # Returned
            return input("Who returned your loan?: ").strip().title()
        elif liable_subtype == Liabili.subtypeChoiceDetail[2][:4].lower(): # Owed
            return input("Who do you owe?: ").strip().title()
        elif liable_subtype == Liabili.subtypeChoiceDetail[3][:4].lower(): # Paid
            return input("Who did you pay back?: ").strip().title()
        else:
            print(f"LIABLE_NAME_ERROR: subtype was not found.\n")



class Savings(LogDetails):
    logTypeDetail = "sav"   # "Savings"
    subtypeChoiceDetail = ["Deposit", "Withdrawal"]