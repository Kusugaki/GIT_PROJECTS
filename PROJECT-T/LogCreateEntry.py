from abc import ABC, abstractmethod

# ABSTRACT CLASS - (dahil trip ko lang)
class LogDetails(ABC):
    logTypeDetail:       str
    subtypeChoiceDetail: list[str] # peaniths
    logTitleDetail:      str

    @classmethod
    def get_log_type(cls) -> str:
        return cls.logTypeDetail[:3].lower()
    
    @classmethod
    def get_log_subtype(cls) -> str:
        user_input:str = None
        while user_input not in ['A','B']:
            user_input = input(f"Enter subtype:\n\tA. \'{cls.subtypeChoiceDetail[0]}\'\n\tB. \'{cls.subtypeChoiceDetail[1]}\'\n  > ").upper()

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
    logTypeDetail = "Transactions"
    subtypeChoiceDetail = ["Debit", "Credit"]

    def get_log_title_from_subtype() -> str:
        return input("Input Log Title: ").strip()

class Liabili(LogDetails):
    logTypeDetail = "Liabilities"
    subtypeChoiceDetail = ["Loaned", "Owed"]

class Savings(LogDetails):
    logTypeDetail = "Savings"
    subtypeChoiceDetail = ["Deposit", "Withdrawal"]




class CreateEntry:
    logType:str
    subtype:str
    title:str

    @classmethod
    def fetch_entry_details(cls) -> None:
        '''Fetches info for LOGTYPE, Log SUBTYPE, and TITLE'''

        user_input = None
        while user_input not in ['A','B','C']:
            user_input = input("""Enter Log Type:\n\tA. \'Transactions\'\n\tB. \'Liabilities\'\n\tC. \'Savings\'\n  > """).upper()

            match user_input:
                case 'A':
                    cls.logType = Transac.get_log_type()
                    cls.subtype = Transac.get_log_subtype()
                    cls.title   = Transac.get_log_title_from_subtype()
                case 'B':
                    cls.logType = Liabili.get_log_type()
                    cls.subtype = Liabili.get_log_subtype()
                    cls.title   = Liabili.get_log_title_from_subtype()
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
            try: return abs(float(input("Input Transaction Amount: ")))
            except ValueError as e: print(f"NaN_ERROR: {e}")

    @staticmethod
    def create_ID(total, logType, subtype, date) -> str:
        '''Creates a unique ID'''
        return f"{total}//{logType}//{subtype}//{date}"

