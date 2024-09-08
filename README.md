# I'm gay 🦌🦌🦌🦌

###### (or am i?)

## Program IDEAS: Functions & Definitions

1. Program automatically updates important changes at startup
2. Automatically determine the date and create a new log once it changes
3. At the end of the day, display out the main compiled auditTrail of all logTypes as one
4. Create attributes for Debit:Credit, Deposit:Withdrawals, and Loaned:Debt
5. All changes in the logs shall automatically be inputted into the Audit Trail
6. A list of methods shall be:  
      - New Transaction (with parameter of logType)  
      - Delete Transaction  
      - Modify Log  
      - Display Log (with parameter of logType)  
      - Display Audit Trail (logs compiler)  
      - Search Logs (using date, day, logType, etc.)  
7. All final changes shall be saved to a .json or .csv file
8. A list of important attributes shall be:  
      - day  
      - date  
      - title (log Title)  
      - amount  
      - logType (transac/savings/lendings)  
      - logID (identifiers for specific logs to modify)  
        - FORMAT ==> %day-%index-%logType (example: 02-253-sav)  
      - logCount (total amount of logs created in the main Audit Trail)  
        - possibly add a checkpoint/achievement system for every "count % 100" logs  

# Supposed Outputs

## Main Log Sample
###### Does not represent final output

| Day | Date     | Transactions | Debit   | Credit   |
| --- | :----    | :----------- | :-----: | :------: |
| 1   | 08-08-24 | Day in       | 213     |          |
| 2   | 08-08-24 | Pamasahe 1   |         | 100      |
| 3   | 08-08-24 | Burgersilog  |         | 36       |
| 4   | 08-08-24 | Day out      | 213     | 136      |

# End of Day Status Screen Sample
###### Only possible ideas

<!-- <code> -->

|                    |         |
| :----------------- | :-----: |
| TOTALS:            |         |
| Initial Day in     | 213     |
| Day out Credit     | 136     |
|                    |         |
|                    |         |
| DETAILS:           |         |
| Saved Amount       | 77      |
| Savings Percentage | 36.15%  | 
|                    |         |
|                    |         |
| EXTRAS:            |         |
| Current Savings    | 3,600   |
| Current Debts      | 0       |
| Unpayed Loans      | 1,200   |

<!-- </code> -->
