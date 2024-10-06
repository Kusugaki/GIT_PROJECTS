# Personal Project 🦌🦌🦌🦌

Project Based Learning for OOP by basing off of mostly only a single youtube video with minimal help from stackoverflow.

Highly recommend for Beginner OOP Introduction: [Python Object Oriented Programming (OOP) - For Beginners (by Tech with Tim)](https://www.youtube.com/watch?v=JeznW_7DlB0)

## To-do List: Ver 1.1

<!-- - [ ] Auto create "Total" rows per new day -->
- [x] Change display_single_entry() to use variables for column widths
- [x] Implement status screen
- [x] Find other lackluster features
- [x] (No longer needed) Automatically create "Previous" log entries
- [x] Create independent 'date_search()' method
- [x] Make a better Status table (abomination 😭)
- [x] Implement Exporting entries

## To-do List: Ver 2.0

- [ ] GUI update
- [x] Lose sanity
- [ ] Regain sanity
- [ ] Find a life
- [ ] Profit

## INITIAL Program Ideas: Functions & Definitions

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

## Supposed Outputs

### Main Log Sample Idea

| Day | Date     | Transactions    | Debit   | Credit   |
| --- | :------- | :-------------- | :-----: | :------: |
| 1   | 08-08-24 | Day in          | 213     |          |
|     |          | Pamasahe 1      |         | 100      |
|     |          | Burgersilog     |         | 36       |
|     |          | Day out (Total) | 213     | 272      |

## End of Day Status Screen Idea

|                    |         |
| :----------------- | :-----: |
| TOTALS:            |         |
| Day out Debit      | 213     |
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

###### shika
