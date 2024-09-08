import json
import csv

class FileGetter():
    def get_path(self, default_path:str) -> str: 
        path_input = input("Enter CSV file path:\n>")
        if path_input == '':
            return default_path
        return path_input
    

    def get_main_log(self):
        return NotImplementedError


class FileSaver():
    def save_previous_entries(self, file_path) -> None:
        csv_writer = csv.reader(file_path)

        with open(file_path, 'w', newline='', encoding="utf-8") as csvFile:
            for entry in self.logList:
                csv_writer.writerow()

    def end_and_save(self, file_path) -> None:
        csv_writer = csv.reader(file_path)

        with open(file_path, 'w', newline='', encoding="utf-8") as csvFile:
            for entry in self.logList:
                csv_writer.writerow()

    
    def save_main_log(self, file_path) -> None:
        csv_writer = csv.reader(file_path)

        with open(file_path, 'w', newline='', encoding="utf-8") as csvFile:
            for entry in self.logList:
                csv_writer.writerow()


if __name__ == '__main__':
    import csv