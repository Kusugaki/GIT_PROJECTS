import os

import AuditManager as AM   # to externally overwrite & configure global variables
from LogTableDisplays import TableDisplays as TD # to externally overwrite & configure global variables
from AuditManager import Auditing, TableDisplays


# AuditManager GLOBAL VARIABLES CONFIG
AM.DEFAULT_FILE_NAME = "audit_database.csv" 
AM.DEFAULT_FILE_PATH = os.path.join(os.path.dirname(__file__), AM.DEFAULT_FILE_NAME)

# TableDisplays ATTRIBUTES CONFIG
TD.MAX_DISPLAY_LIMIT = 150


class Main():
    def main() -> None:
        audit = Auditing()

        spacing:int= 80
        user:str   = None
        status:int = None

        while user != 0:
            try:
                print("What to do?:")
                print("\t  1. \'Create Entry\'") 
                print("\t  2. \'Modify Entry\'") 
                print("\t  3. \'Delete Entry\'") 
                print("\t  4. \'Display Specified Status\'")
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
                if status == 1: print("\n" ," Entry successfully created! ".center(spacing,"~"), "\n")
                else:           print("\n" ," Entry creation failed... ".center(spacing,"~"), "\n")

            elif user == 2: # Modify an Entry
                status = audit.modify_entry()
                if status == 1: print("\n" ," Entry successfully modified! ".center(spacing,"~"), "\n")
                else:           print("\n" ," Entry modification failed... ".center(spacing,"~"), "\n")

            elif user == 3: # Delete an Entry
                status = audit.delete_entry()
                if status == 1: print("\n" ," Entry successfully deleted! ".center(spacing,"~"), "\n")
                else:           print("\n" ," Entry deletion failed... ".center(spacing,"~"), "\n")

            elif user == 4: # Display STATUS table
                audit.display_status()

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
                print("\n" ," Saved all Entries! ".center(spacing,"~"), "\n")

            elif user == 444: # DEBUG display
                audit.debug_display_entries()

            elif user == 555: # DEBUG Search for specific categories
                status = audit.search_entry()

                if status != None: 
                    TableDisplays.debug_display_table_single_entry(Auditing.mainLogList[status], show_header=True)
                    print("\n" ," Entry search success! ".center(spacing,"~"), "\n")
                else:              
                    print("\n" ," Entry search failed... ".center(spacing,"~"), "\n")

        audit.save_all_entries()
        print("\n", f"\'{AM.DEFAULT_FILE_PATH}\' saved successfully".center(100,"~"))
        print("exiting...")
        del audit
        return
    



if __name__ == '__main__':
    print("/","".center(50,"-"),"\\")
    print("|","Welcome to Audit Manager v.1".center(50,"-"),"|")
    print("\\","".center(50,"-"),"/")

    Main.main()