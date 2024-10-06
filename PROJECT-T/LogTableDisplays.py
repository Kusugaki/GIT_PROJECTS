class TableDisplays():
    MAX_DISPLAY_LIMIT:int = 100
    
    '''Table column width "percentages" '''
    percount   = 5
    perday     = 3
    perdate    = 12
    perlogtype = 7
    persubtype = 7
    pertitle   = 25
    peramount  = 13
    perID      = 30
    perliaName = 15

    perdebit   = peramount
    percredit  = peramount - 1

    @classmethod
    def display_table(cls, logList:list[object], specifiedLogtype:list[str], debitList:list[str]) -> None:
        perTotal = cls.percount + cls.perday + cls.perdate + cls.pertitle + cls.perdebit + cls.percredit + 17 # accounting for table vertical line spacings
        prevDate = None

        '''Show header'''
        print(f" {"":_<{perTotal}}")
        print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"TITLE":^{cls.pertitle}} | {"DEBIT":^{cls.perdebit}} | {"CREDIT":^{cls.percredit}} |")
        for entry in logList[-cls.MAX_DISPLAY_LIMIT-1:]:

            if entry.logType in specifiedLogtype:

                if prevDate != entry.date:
                    '''add linebreaks between new dates'''
                    print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.perdebit}}-|-{"":-<{cls.percredit}}-|")
                    '''only shows day and date once per new date'''
                    if entry.subtype in debitList:
                        print(f"| {entry.count:<{cls.percount}} | {entry.day:^{cls.perday}} | {entry.date:^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {entry.amount:^{cls.perdebit}} | {"":^{cls.percredit}} |")
                    else:   # loaned, paid
                        print(f"| {entry.count:<{cls.percount}} | {entry.day:^{cls.perday}} | {entry.date:^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {"":^{cls.perdebit}} | {entry.amount:^{cls.percredit}} |")
                    prevDate = entry.date
                else:
                    '''no longer shows day and date'''
                    if entry.subtype in debitList:
                        print(f"| {entry.count:<{cls.percount}} | {"":^{cls.perday}} | {"":^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {entry.amount:^{cls.perdebit}} | {"":^{cls.percredit}} |")
                    else:   # credit
                        print(f"| {entry.count:<{cls.percount}} | {"":^{cls.perday}} | {"":^{cls.perdate}} | {entry.title:<{cls.pertitle}} | {"":^{cls.perdebit}} | {entry.amount:^{cls.percredit}} |")
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.perdebit}}-|-{"":-<{cls.percredit}}-|")
        print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"TITLE":^{cls.pertitle}} | {"DEBIT":^{cls.perdebit}} | {"CREDIT":^{cls.percredit}} |")
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.perdebit}}-|-{"":-<{cls.percredit}}-|")
    
    @classmethod
    def display_status_table(cls, debi, cred, loan, retu, owed, paid, depo, draw, netTotal, netPercent, netLoans, netDebts, netSavings):
        amountWidth = cls.peramount + 5
        netPercent = str(round(netPercent*100, 2)) + "%"
        print(f" {"":_<{cls.pertitle + amountWidth + 5}}")
        print(f"| {      "TOTALS"       :^{cls.pertitle}} | {"AMOUNT"  :^{amountWidth}} |")
        print(f"| {"  Total Saved"      :<{cls.pertitle}} | {debi      :^{amountWidth}} |")
        print(f"| {"  Total Loss"       :<{cls.pertitle}} | {cred      :^{amountWidth}} |")
        print(f"| {""                   :^{cls.pertitle}} | {""        :<{amountWidth}} |")
        print(f"| {"  Total Loaned"     :<{cls.pertitle}} | {loan      :^{amountWidth}} |")
        print(f"| {"  Total Returns"    :<{cls.pertitle}} | {retu      :^{amountWidth}} |")
        print(f"| {""                   :^{cls.pertitle}} | {""        :<{amountWidth}} |")
        print(f"| {"  Total Owed"       :<{cls.pertitle}} | {owed      :^{amountWidth}} |")
        print(f"| {"  Total Payments"   :<{cls.pertitle}} | {paid      :^{amountWidth}} |")
        print(f"| {""                   :^{cls.pertitle}} | {""        :<{amountWidth}} |")
        print(f"| {"  Total Deposits"   :<{cls.pertitle}} | {depo      :^{amountWidth}} |")
        print(f"| {"  Total Withdrawals":<{cls.pertitle}} | {draw      :^{amountWidth}} |")
        print(f"|-{"------------------":-<{cls.pertitle}}-|-{"-------":-<{amountWidth}}-|")
        print(f"| {      "DETAILS"      :^{cls.pertitle}} | {""        :^{amountWidth}} |")
        print(f"| {"  Net Amount"       :<{cls.pertitle}} | {netTotal  :^{amountWidth}} |")
        print(f"| {"  Net Percentage"   :<{cls.pertitle}} | {netPercent:^{amountWidth}} |")
        print(f"|-{"------------------":-<{cls.pertitle}}-|-{"-------":-<{amountWidth}}-|")
        print(f"| {      "EXTRAS"       :^{cls.pertitle}} | {""        :^{amountWidth}} |")
        print(f"| {"  Current Savings"  :<{cls.pertitle}} | {netSavings:^{amountWidth}} |")
        print(f"| {"  Unpayed Debts"    :<{cls.pertitle}} | {netDebts  :^{amountWidth}} |")
        print(f"| {"  Unpayed Lendings" :<{cls.pertitle}} | {netLoans  :^{amountWidth}} |")
        print(f"|-{"":-<{cls.pertitle}}-|-{"":-<{amountWidth}}-|")


    @classmethod
    def debug_display_table(cls, logList:list[object], filtered=False, search_parameter=None) -> None:
        perTotal = cls.percount + cls.perday + cls.perdate + cls.perlogtype + cls.persubtype + cls.pertitle + cls.peramount + cls.perID + cls.perliaName + 27 # accounting for table vertical line spacings

        print(f" {"":_<{perTotal-1}}")
        
        for entry in logList[-cls.MAX_DISPLAY_LIMIT-1:]:
            if not filtered:
                cls.debug_display_table_single_entry(entry)
            elif search_parameter in entry.logType or search_parameter in entry.subtype:
                cls.debug_display_table_single_entry(entry)
                                                                        # (-) note: REMOVE THESE PLACEHOLDER LIABILITY NAMES
            elif search_parameter in entry.liaName and entry.liaName != "~~~~~~~" and entry.liaName != "NON-LIA" and entry.liaName != "NOT_SET":
                cls.debug_display_table_single_entry(entry)

        '''Show footer details'''
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")
        print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"LOGTYPE":^{cls.perlogtype}} | {"SUBTYPE":^{cls.persubtype}} | {"TITLE":^{cls.pertitle}} | {"AMOUNT":^{cls.peramount}} | {"LOG ID":^{cls.perID}} | {"LIABLE NAME":^{cls.perliaName}} |")
        print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")

    @classmethod
    def debug_display_table_single_entry(cls, entry, show_header=False) -> None:
        if show_header == False:
            '''Used for displaying whole table'''
            print(f"| {entry.count:<{cls.percount}} | {entry.day:<{cls.perday}} | {entry.date:<{cls.perdate}} | {entry.logType:<{cls.perlogtype}} | {entry.subtype:<{cls.persubtype}} | {entry.title:<{cls.pertitle}} | {entry.amount:<{cls.peramount}} | {entry.logID:<{cls.perID}} | {entry.liaName:<{cls.perliaName}} |")
        else:
            '''Used for entry deletion and modification visual confirmation'''
            print(f" {"":_<{cls.percount + cls.perday + cls.perdate + cls.perlogtype + cls.persubtype + cls.pertitle + cls.peramount + cls.perID + cls.perliaName + 26}}")
            print(f"| {"COUNT":^{cls.percount}} | {"DAY":^{cls.perday}} | {"DATE":^{cls.perdate}} | {"LOGTYPE":^{cls.perlogtype}} | {"SUBTYPE":^{cls.persubtype}} | {"TITLE":^{cls.pertitle}} | {"AMOUNT":^{cls.peramount}} | {"LOG ID":^{cls.perID}} | {"LIABLE NAME":^{cls.perliaName}} |")
            print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")
            print(f"| {entry.count:<{cls.percount}} | {entry.day:<{cls.perday}} | {entry.date:<{cls.perdate}} | {entry.logType:<{cls.perlogtype}} | {entry.subtype:<{cls.persubtype}} | {entry.title:<{cls.pertitle}} | {entry.amount:<{cls.peramount}} | {entry.logID:<{cls.perID}} | {entry.liaName:<{cls.perliaName}} |")
            print(f"|-{"":-<{cls.percount}}-|-{"":-<{cls.perday}}-|-{"":-<{cls.perdate}}-|-{"":-<{cls.perlogtype}}-|-{"":-<{cls.persubtype}}-|-{"":-<{cls.pertitle}}-|-{"":-<{cls.peramount}}-|-{"":-<{cls.perID}}-|-{"":-<{cls.perliaName}}-|")
    
            # print("|-{0:<{1}}-|-{1:<{cls.perday}}-|-{2:<{cls.perdate}}-|-{3:<{cls.perlogtype}}-|-{4:<{cls.persubtype}}-|-{5:<{cls.pertitle}}-|-{6:<{cls.peramount},f}-|-{7:<{cls.perID}}-|-{8:<{cls.perliaName}}-|".format("", "", "", "", "", "", "", "", ""))
            # print("| {0:<{1}} | {1:<{cls.perday}} | {2:<{cls.perdate}} | {3:<{cls.perlogtype}} | {4:<{cls.persubtype}} | {5:<{cls.pertitle}} | {6:<{cls.peramount},f} | {7:<{cls.perID}} | {8:<{cls.perliaName}} |".format(entry.count, entry.day, entry.date, entry.logType, entry.subtype, entry.title, entry.amount, entry.logID, entry.liaName))
            # print("|-{0:<{1}}-|-{1:<{cls.perday}}-|-{2:<{cls.perdate}}-|-{3:<{cls.perlogtype}}-|-{4:<{cls.persubtype}}-|-{5:<{cls.pertitle}}-|-{6:<{cls.peramount},f}-|-{7:<{cls.perID}}-|-{8:<{cls.perliaName}}-|".format("", "", "", "", "", "", "", "", ""))
