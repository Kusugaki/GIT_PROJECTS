def debug(output:str="", addNotif:bool=True) -> None:
    if addNotif is True:
        print(f"DEBUG: {output}")
    else:
        print(f"{output}")