from LogEntry_dataclass import LogEntry
import csv
import os

class FileGetter():
    fetched_list: list[object] = []

    @classmethod
    def fetch_saved_database(cls, path:str) -> list:
        if not os.path.exists(path):
            print(f"no database found in \'{path}\'.")
            return []

        with open(path, 'r', encoding="utf-8") as csv_file:
            csv_reader: csv = csv.reader(csv_file)

            line: int = 0
            for row in csv_reader:
                if not line == 0:   # SKIP HEADER ROW
                    cls.get_fetched_list().append(
                        LogEntry(
                            total   = row[0],
                            date    = row[1],
                            logType = row[2], 
                            subtype = row[3],
                            title   = row[4],   
                            amount  = row[5],
                            logID   = row[6]
                        )
                    )
                line += 1

        return cls.get_fetched_list()


    @classmethod
    def get_fetched_list(cls):
        return cls.fetched_list

    @staticmethod
    def get_custom_path(default_path:str) -> str: 
        path_input = input("Enter CSV file path:\n>")
        if path_input == '':
            return default_path
        return path_input
    

class FileSaver():
    @staticmethod
    def save_data(dict:dict, path: str) -> bool:
        if not os.path.exists(path):
            with open(path, 'w', newline='', encoding="utf-8") as csv_header:
                csv_writer = csv.writer(csv_header)
                csv_writer.writerow(["TOTAL", "DATE", "LOGTYPE", "SUBTYPE", "TITLE", "AMOUNT", "LOG-ID"])
                print("Created a NEW csv file since none was found")

        with open(path, 'a', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(
                    [
                        dict["total"],
                        dict["date"],
                        dict["logType"],
                        dict["subtype"],
                        dict["title"],
                        dict["amount"],
                        dict["logID"]
                    ]
                )




if __name__ == '__main__':
    ...