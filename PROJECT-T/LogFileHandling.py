import csv
import os

from abc import ABC, abstractmethod

from LogEntry_dataclass import LogEntry


class FileHandler(ABC):
    @abstractmethod
    def get_custom_path():
        pass


class FileGetter(FileHandler):
    fetched_list: list[LogEntry] = []
    fetched_todayList: list[LogEntry] = []

    @classmethod
    def fetch_saved_database(cls, path:str) -> list[LogEntry]:
        
        if not os.path.exists(path):
            print(f"no database found in \'{path}\'.")
            return []
        
        try:
            with open(path, 'r', encoding="utf-8") as csv_file:
                csv_reader: csv = csv.reader(csv_file)
                next(csv_reader)

                for row in csv_reader:
                        cls.fetched_list.append(
                            LogEntry(
                                count   = int(row[0]),
                                day     = int(row[1]),
                                date    = row[2],
                                logType = row[3], 
                                subtype = row[4],
                                title   = row[5],   
                                amount  = float(row[6]),
                                logID   = row[7],
                                liaName = row[8]
                            )
                        )
        except Exception as e:
            print(f"ERROR_READING_FILE \'{path}\': {e}")

        return cls.fetched_list

    @classmethod
    def fetch_curr_list(cls, dateToday:str) -> list[LogEntry]:
        return [obj for obj in cls.fetched_list if obj.date == dateToday]

    @staticmethod
    def get_custom_path(default_path:str) -> str: 
        path_input = input("Enter CSV file path:\n>").strip()
        if path_input == '':
            print("No input, going with DEFAULT path.")
            return default_path
        return path_input
    

class FileSaver(FileHandler):
    @staticmethod
    def save_and_append_data(dict:dict, path: str) -> bool:
        ''' appends new data to csv file '''
        try:
            if not os.path.exists(path):
                with open(path, 'w', newline='', encoding="utf-8") as csv_header:
                    csv_writer = csv.writer(csv_header)
                    csv_writer.writerow(["COUNT", "DAY", "DATE", "LOGTYPE", "SUBTYPE", "TITLE", "AMOUNT", "LOG-ID", "LIABLE NAME"])
                    print("Created a NEW csv file since none was found")

            with open(path, 'a', newline='', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([
                    dict["count"],
                    dict["day"],
                    dict["date"],
                    dict["logType"],
                    dict["subtype"],
                    dict["title"],
                    dict["amount"],
                    dict["logID"],
                    dict["liaName"]
                ])
            return True
        except Exception as e:
            print(f"ERROR_SAVING_FILE \'{path}\': {e}")
            return False

    @staticmethod
    def save_all_data(mainlog:list, path: str) -> bool:
        ''' overwrites whole csv file '''
        try:
            if not os.path.exists(path):
                with open(path, 'x') as created_file:
                    print("Created a NEW csv file since none was found")

            with open(path, 'w', newline='', encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["COUNT", "DAY", "DATE", "LOGTYPE", "SUBTYPE", "TITLE", "AMOUNT", "LOG-ID", "LIABLE NAME"])
                
                for entry in mainlog:
                    entryDict = entry.__dict__

                    csv_writer.writerow([
                        entryDict["count"],
                        entryDict["day"],
                        entryDict["date"],
                        entryDict["logType"],
                        entryDict["subtype"],
                        entryDict["title"],
                        entryDict["amount"],
                        entryDict["logID"],
                        entryDict["liaName"]
                    ])
            return True
        except Exception as e:
            print(f"ERROR_SAVING_FILE \'{path}\': {e}")
            return False
        
    @staticmethod
    def get_custom_path(default_path:str) -> str: 
        path_input:str = ''

        while True:
            path_input = input("Enter custom file name:\n>").strip().replace(' ', '')
            if path_input == '':
                print("\tPlease input something.\n")
                continue
        
            path_input += ".csv"
            custom_path = os.path.join(default_path, path_input)

            if os.path.exists(custom_path):
                overwrite = input("File already exists... Overwrite? (y/n)\n\t> ")
                if overwrite == 'y':
                    break
                else:
                    continue
            break
        return custom_path



if __name__ == '__main__':
    ''' 
        abstract class testing, cannot instantiate an object without defining 
        abstract method first but the other methods can be used by other modules 
        as long as an object is not instantiated for the FileSaver / FileGetter classes
    '''
    print(f"YOU ARE RUNNING {__file__}!!!")

    sav = FileSaver()
    get = FileGetter()