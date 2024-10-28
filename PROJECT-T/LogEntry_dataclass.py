from dataclasses import dataclass

@dataclass(kw_only=True)
class LogEntry:
    count:   int   = 0
    day:     int   = 0
    date:    str   = "NOT_SET"    
    logType: str   = "NOT_SET" 
    subtype: str   = "NOT_SET" 
    title:   str   = "NOT_SET"
    amount:  float = 0.0
    logID:   str   = "NOT_SET"
    liaName: str   = "NOT_SET"
