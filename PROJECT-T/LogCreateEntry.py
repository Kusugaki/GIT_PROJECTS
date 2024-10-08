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
    




class LogDetails:
    logTypeDetail:       str
    subtypeChoiceDetail: list[str] # peaniths
    logTitleDetail:      str

    @classmethod
    def get_log_type(cls) -> str:
        return cls.logTypeDetail
    
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
    def get_log_title_from_subtype(cls) -> str:
        return cls.logTitleDetail





class Transac(LogDetails):
    logTypeDetail = "tra" # "Transactions"
    subtypeChoiceDetail = ["Debit", "Credit"]

    @staticmethod
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

    @classmethod
    def get_liable_entity(cls, liable_subtype) -> str:
        charLimit:int = 11  # Based off of the CLI table display 'title' column width
        name:str
        
        while True:
            if   liable_subtype == Liabili.subtypeChoiceDetail[0][:4].lower(): # Loaned
                name = input("Loaned to whom?: ").strip().title()
                cls.logTitleDetail = cls.subtypeChoiceDetail[0]
            elif liable_subtype == Liabili.subtypeChoiceDetail[1][:4].lower(): # Returned
                name = input("Who returned your loan?: ").strip().title()
                cls.logTitleDetail = cls.subtypeChoiceDetail[1]
            elif liable_subtype == Liabili.subtypeChoiceDetail[2][:4].lower(): # Owed
                name = input("Who do you owe?: ").strip().title()
                cls.logTitleDetail = cls.subtypeChoiceDetail[2]
            elif liable_subtype == Liabili.subtypeChoiceDetail[3][:4].lower(): # Paid
                name = input("Who did you pay back?: ").strip().title()
                cls.logTitleDetail = cls.subtypeChoiceDetail[3]
            else:
                print(f"LIABLE_NAME_ERROR: subtype was not found.\n")

            if len(name) <= charLimit:
                break
        
            print("Name is too long, maximum of 11 characters only\n")

        return name



class Savings(LogDetails):
    logTypeDetail = "sav"   # "Savings"
    subtypeChoiceDetail = ["Deposit", "Withdrawal"]
