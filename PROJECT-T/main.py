import os

import AuditManager
from AuditManager import Auditing, TableDisplays

# GLOBAL VARIABLES
DEFAULT_FILE_NAME:str = AuditManager.DEFAULT_FILE_NAME 
DEFAULT_FILE_PATH:str = AuditManager.DEFAULT_FILE_PATH
MAX_DISPLAY_LIMIT:int = AuditManager.MAX_DISPLAY_LIMIT



class Main():
    def main() -> None:
        audit = Auditing()

        user:str   = None
        status:int = None

        while user != 0:
            try:
                print("What to do?:")
                print("\t  1. \'Create Entry\'") 
                print("\t  2. \'Modify Entry\'") 
                print("\t  3. \'Delete Entry\'") 
                print("\t  4. \'Use Search Filter\'")
                print("\t  5. \'Display Transactions\'")
                print("\t  6. \'Display Liabilities\'")
                print("\t  7. \'Display Savings\'")
                print("\t  8. \'Display all Entries\'") 
                print("\t  9. \'Save all Entries\'") 
                print("\t  0. \'Save and Exit\'") 

                user = int(input("   > ").strip())
            except ValueError as e: 
                print(f"INVALID_INPUT: {e}")
                continue

            if   user == 1: # Create an Entry
                status = audit.create_entry()
                if status == 1: print("\n" ," Entry successfully created! ".center(54,"~"), "\n")
                else:           print("\n" ," Entry creation failed... ".center(54,"~"), "\n")

            elif user == 2: # Modify an Entry
                status = audit.modify_entry()
                if status == 1: print("\n" ," Entry successfully modified! ".center(54,"~"), "\n")
                else:           print("\n" ," Entry modification failed... ".center(54,"~"), "\n")

            elif user == 3: # Delete an Entry
                status = audit.delete_entry()
                if status == 1: print("\n" ," Entry successfully deleted! ".center(54,"~"), "\n")
                else:           print("\n" ," Entry deletion failed... ".center(54,"~"), "\n")

            elif user == 4: # Search for specific categories
                '''(-) note: debug option, can be changed for something else'''
                status = audit.search_entry()

                if status != None: 
                    TableDisplays.debug_display_table_single_entry(Auditing.mainLogList[status], show_header=True)
                    print("\n" ," Entry search success! ".center(54,"~"), "\n")
                else:              
                    print("\n" ," Entry search failed... ".center(54,"~"), "\n")

            elif user == 5: # Display all TRANSACTIONS
                audit.display_transactions()

            elif user == 6: # Displays all LIABILITIES
                audit.display_liabilities()

            elif user == 7: # Displays all SAVINGS
                audit.display_savings()

            elif user == 8: # Display ALL ENTRIES
                audit.display_all_entries()

            elif user == 9: # Save all Entries
                status = audit.save_all_entries()
                print("\n" ," Saved all Entries! ".center(54,"~"), "\n")

            elif user == 444: # DEBUG display
                audit.debug_display_entries()

        audit.save_all_entries()
        print(f"\'{DEFAULT_FILE_PATH}\' saved successfully".center(100,"~"), "\n")
        print("exiting...")
        del audit
        return






if __name__ == '__main__':
    print("/","".center(50,"-"),"\\")
    print("|","Welcome to Audit Manager v.1".center(50,"-"),"|")
    print("\\","".center(50,"-"),"/")

    Main.main()