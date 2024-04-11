#######################################
# IMPORTS
#######################################

import random
import string
import inspect

from PyEssentials.errors import InvalidPrefix

from colorama import init, Fore, Back, Style

#######################################
# INIT
#######################################

init(convert=True)

#######################################
# VARIABLES
#######################################

NUMBERS = "0123456789"
UPPERS  = string.ascii_uppercase
LOWERS  = string.ascii_lowercase

#######################################
# FUNCTIONS
#######################################

def PrintError(error) -> int:
    """
    ## Print error with red foreground.
    """
    print(f"{Fore.RED}{error}{Style.RESET_ALL}")
    return 0

def generate_id(length: int=16, numbers: bool=True, lowers: bool=True, uppers: bool=True) -> str:
    """
    ## Generate ID with numbers, uppercase and lowercase letters.

    ### Example of generated ID: 
    * 7wCxklbqgbXkO0K6
    """
    chars = ""
    if numbers: chars += NUMBERS
    if lowers: chars += LOWERS
    if uppers: chars += UPPERS

    return ''.join(random.choice(chars) for _ in range(length))

def generate_custom_id(prefix: str, length: int=16) -> str:
    """
    ## Generate custom ID with numbers, uppercase and lowercase letters.

    ### How to write prefix?
    * Prefix must not be None.
    * Prefix must not have any numbers or special characters

    ### Example of generated custom ID: 
    * $CR#7wCxklbqgbXkO0K6
    """
    if not prefix: 
        PrintError(InvalidPrefix(prefix))
        return None
    else: 
        for c in prefix:
            if not c in UPPERS + LOWERS:
                PrintError(InvalidPrefix(prefix))
                return None
        return f"${prefix}#" + generate_id(length)
    
def check_command_func(func) -> bool:
    """
    ## Check if command function is valid.
    """
    signature = inspect.signature(func)
    params = signature.parameters

    first_param_name = next(iter(params))
    first_param = params[first_param_name]

    try:
        if first_param.annotation == list[str]:
            return signature.return_annotation == int
        else:
            return False
    except:
        return False