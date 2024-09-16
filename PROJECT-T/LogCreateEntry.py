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

            match user_input:
                case 'A':
                    cls.logType = Transac.get_log_type()
                    cls.subtype = Transac.get_log_subtype()
                    cls.title   = Transac.get_log_title_from_subtype()
                case 'B':
                    cls.logType = Liabili.get_log_type()
                    cls.subtype = Liabili.get_log_subtype()
                    cls.liaName = Liabili.get_liable_entity(cls.subtype)
                    cls.title   = Liabili.get_log_title_from_subtype(cls.liaName)
                case 'C':
                    cls.logType = Savings.get_log_type()
                    cls.subtype = Savings.get_log_subtype()
                    cls.title   = Savings.get_log_title_from_subtype()
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")
                    continue

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

            match user_input:
                case 'A':
                    cls.logTitleDetail = cls.subtypeChoiceDetail[0]
                    return cls.subtypeChoiceDetail[0][:4].lower()
                
                case 'B':
                    cls.logTitleDetail = cls.subtypeChoiceDetail[1]
                    return cls.subtypeChoiceDetail[1][:4].lower()
                
                case _:
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
    subtypeChoiceDetail = ["Loaned", "Owed"]
        
    @classmethod
    def get_log_title_from_subtype(cls, name) -> str:
        return f"{cls.logTitleDetail} -> ({name})"

    @staticmethod
    def get_liable_entity(liable_subtype) -> str:
        if liable_subtype == Liabili.subtypeChoiceDetail[0]: # Loaned
            return input("Loaned to whom?: ").strip().title()
        else: # Owed
            return input("Who do you owe?: ").strip().title()


class Savings(LogDetails):
    logTypeDetail = "sav"   # "Savings"
    subtypeChoiceDetail = ["Deposit", "Withdrawal"]