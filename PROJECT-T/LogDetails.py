from abc import ABC, abstractmethod

# ABSTRACT CLASS - (dahil trip ko lang)
class LogDetails(ABC):
    titleChoice:str
    subtype:str

    @classmethod
    @abstractmethod # not an actual abstract method, child classes don't actually modify or specialize the method individually
    def fetch_entry_details(cls, choicesList, subtypeIDlist) -> None:
        _user_input = None
        
        while _user_input not in ['A','B']: 
            _user_input = input(f"""Enter Log Type:\n\tA. \'{choicesList[0]}\'\n\tB. \'{choicesList[1]}\'\n  > """).upper()

            match _user_input:
                case 'A':
                    cls.titleChoice = choicesList[0]
                    cls.subtype     = subtypeIDlist[0]
                case 'B':
                    cls.titleChoice = choicesList[1]
                    cls.subtype     = subtypeIDlist[1]
                case _:
                    print(f"INPUT_ERROR: \'{_user_input}\' is not part of the options.\n")
                    continue


class Transac(LogDetails):
    logType:str = "tra"
    def fetch_entry_details() -> None:
        LogDetails.fetch_entry_details(["Debit", "Credit"], ["debi", "cred"])

class Liabili(LogDetails):
    logType:str = "lia"
    def fetch_entry_details() -> None:
        LogDetails.fetch_entry_details(["Loaned", "Owed"], ["loan", "owed"])

class Savings(LogDetails):
    logType:str = "sav"
    def fetch_entry_details() -> None:
        LogDetails.fetch_entry_details(["Deposit", "Withdrawal"], ["depo", "draw"])
    

    

if __name__ == '__main__':
    print("You are running the LogDetails.py file")
    t = Transac.fetch_entry_details()
    l = Liabili.fetch_entry_details()
    s = Savings.fetch_entry_details()
    print(f"{t = }")
    print(f"{l = }")
    print(f"{s = }")