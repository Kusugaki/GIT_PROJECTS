from dataclasses import dataclass

@dataclass(kw_only=True)
class LogEntry:
    total:   int    = 0
    date:    str    = "DEFAULT"    
    logType: str    = "DEFAULT" 
    subtype: str    = "DEFAULT" 
    title:   str    = "DEFAULT"   
    amount:  float  = 0.0
    logID:   str    = "DEFAULT"