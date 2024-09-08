from abc import ABC, abstractmethod

# ABSTRACT CLASS - (dahil trip ko lang)
class LogMetadata(ABC):
    # @staticmethod
    # def get_value_at_index(__list, index):
    #     return __list[index]
    subtype:str
    logType:str
    titleChoice:str

    @classmethod
    @abstractmethod # not an actual abstract method, child classes don't actually modify or specialize the method individually
    def fetch_metadata_details(cls, choicesList, subtypeIDlist) -> None:
        options = ['A','B']
        _user_input = None
        
        for i in range(5):
            _user_input = input(f"""Enter Log Type:\n\tA. \'{choicesList[0]}\'\n\tB. \'{choicesList[1]}\'\n  > """).upper()
            
            try: 
                assert _user_input in options 
                break
            except AssertionError: print(f"ASSERTION_ERROR: \'{_user_input}\' is not in the Options.\n")
        else:
            print("FAILED TO INPUT TRANSACTION SUBTYPE\n") 

        match _user_input:
            case 'A':
                cls.titleChoice = choicesList[0]
                cls.subtype     = subtypeIDlist[0]
            case 'B':
                cls.titleChoice = choicesList[1]
                cls.subtype     = subtypeIDlist[1]
            case _:
                print(f"LOG_SELECTION_ERROR: DEFAULTING TO \'{subtypeIDlist[0]}\' LOG_SUBTYPE")
                cls.titleChoice = choicesList[0]
                cls.subtype     = subtypeIDlist[0]


class Transac(LogMetadata):
    logType:str = "tra"
    def fetch_metadata_details() -> None:
        LogMetadata.fetch_metadata_details(["Debit", "Credit"], ["debi", "cred"])

class Liabili(LogMetadata):
    logType:str = "lia"
    def fetch_metadata_details() -> None:
        LogMetadata.fetch_metadata_details(["Loaned", "Owed"], ["loan", "owed"])

class Savings(LogMetadata):
    logType:str = "sav"
    def fetch_metadata_details() -> None:
        LogMetadata.fetch_metadata_details(["Deposit", "Withdrawal"], ["depo", "draw"])
    

    

if __name__ == '__main__':
    t = Transac.fetch_metadata_details()
    l = Liabili.fetch_metadata_details()
    s = Savings.fetch_metadata_details()
    print(f"{t = }")
    print(f"{l = }")
    print(f"{s = }")