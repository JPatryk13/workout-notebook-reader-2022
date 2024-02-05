def yes_or_no(msg: str) -> bool:
    option = input(msg + " (y/n) ")
    if option == 'y':
        return True
    else:
        return False
