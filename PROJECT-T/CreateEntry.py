from abc import ABC, abstractmethod

# ABSTRACT CLASS - (dahil trip ko lang)
class LogDetails(ABC):
    logTypeDetail:str
    subtypeChoiceDetail:list[str]
    titleDetail:str

    @classmethod
    @abstractmethod
    def get_log_type(cls) -> str:
        return cls.logTypeDetail[:3].lower()
    
    @classmethod
    @abstractmethod
    def get_log_subtype(cls) -> str:
        user_input:str = None
        while user_input not in ['A','B']:
            user_input = input(f"Enter subtype:\n\tA. \'{cls.subtypeChoiceDetail[0]}\'\n\tB. \'{cls.subtypeChoiceDetail[1]}\'\n  > ").upper()

            match user_input:
                case 'A':
                    cls.titleDetail = cls.subtypeChoiceDetail[0]
                    return cls.subtypeChoiceDetail[0][:4].lower()
                case 'B':
                    cls.titleDetail = cls.subtypeChoiceDetail[1]
                    return cls.subtypeChoiceDetail[1][:4].lower()
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

    @classmethod
    @abstractmethod
    def get_log_title_from_log_type(cls) -> str:
        return cls.titleDetail




class Transac(LogDetails):
    logTypeDetail = "Transactions"
    subtypeChoiceDetail = ["Debit", "Credit"]

    def get_log_title_from_log_type() -> str:
        return input("Input Log Title: ").strip()

class Liabili(LogDetails):
    logTypeDetail = "Liabilities"
    subtypeChoiceDetail = ["Loaned", "Owed"]

class Savings(LogDetails):
    logTypeDetail = "Savings"
    subtypeChoiceDetail = ["Deposit", "Withdrawal"]




class CreateEntry:
    def init_fetch_logType(self) -> str:
        user_input = None
        while user_input not in ['A','B','C']:
            user_input = input("""Enter Log Type:\n\tA. Transactions\'\n\tB. \'Liabilities\'\n\tC. \'Savings\'\n""").strip().upper()

            match user_input:
                case 'A':
                    return Transac.get_log_type()
                case 'B':
                    return Liabili.get_log_type()
                case 'C':
                    return Savings.get_log_type()
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")

    def fetch_subtype(self) -> str:
        user_input:str = None
        while user_input not in ['A','B']:
            user_input = input(f"Enter subtype:\n\tA. \'{cls.subtypeChoiceDetail[0]}\'\n\tB. \'{cls.subtypeChoiceDetail[1]}\'\n  > ").upper()

            match user_input:
                case 'A':
                    return cls.subtypeChoiceDetail[0][:4].lower()
                case 'B':
                    return cls.subtypeChoiceDetail[1][:4].lower()
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")



    def init_fetch_entry_details(self) -> None:
        '''Fetches info for LOGTYPE, Log SUBTYPE, and TITLE'''

        user_input = None
        while user_input not in ['A','B','C']:
            user_input = input("""Enter Log Type:\n\tA. \'Transactions\'\n\tB. \'Liabilities\'\n\tC. \'Savings\'\n  > """).upper()

            match user_input:
                case 'A':
                    self.logType = Transac.get_log_type()
                    self.subtype = Transac.get_log_subtype()
                    self.title   = Transac.get_log_title_from_log_type()
                case 'B':
                    self.logType = Liabili.get_log_type()
                    self.subtype = Liabili.get_log_subtype()
                    self.title   = Liabili.get_log_title_from_log_type()
                case 'C':
                    self.logType = Savings.get_log_type()
                    self.subtype = Savings.get_log_subtype()
                    self.title   = Savings.get_log_title_from_log_type()
                case _:
                    print(f"INPUT_ERROR: \'{user_input}\' is not part of the options.\n")
                    continue



    def init_fetch_amount(self) -> float:
        while self.amount == 0:
            try: return abs(float(input("Input Transaction Amount: ")))
            except ValueError as e: print(f"NaN_ERROR: {e}")

    def init_fetch_total_count(self) -> int:
        '''Fetches the total count of log Entries in the dynamic main list'''
        return self.get_total_entry_count()

    def init_create_ID(self) -> str:
        '''Creates a unique ID'''
        return f"{self.total}//{self.logType}//{self.subtype}//{self.date}"

