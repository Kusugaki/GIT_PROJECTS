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

    

if __name__ == '__main__':
    print("You are running the LogDetails.py file")
    print()
    print(f"{Transac.get_log_type() = }\n{Transac.get_log_subtype() = }\n{Transac.get_log_title_from_log_type() = }")
    print(f"{Liabili.get_log_type() = }\n{Liabili.get_log_subtype() = }\n{Liabili.get_log_title_from_log_type() = }")
    print(f"{Savings.get_log_type() = }\n{Savings.get_log_subtype() = }\n{Savings.get_log_title_from_log_type() = }")
