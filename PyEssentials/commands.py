#######################################
# IMPORTS
#######################################

from PyEssentials.errors import *
from PyEssentials.functions import check_command_func, PrintError

from typing import Callable

#######################################
# CLASSES
#######################################

class CommandBase:
    def __init__(self, name: str, func: Callable) -> None:
        self.name = name
        self.func = func

    def Run(self, args: list[str]) -> int:
        return self.func(args)

    def __repr__(self) -> str:
        return f"Command '{self.name}'"

class CommandRegister:
    """
    ## The command register is used to make command management easier.

    ### Features:
    * Adding commands
    * Deleting commands
    * Handling commands or entire inputs
    """
    def __init__(self) -> None:
        self.commands: list[CommandBase] = []
        self.print_errors = True

    def AddCommand(self, name: str, func: Callable[[list[str]], int]) -> int:
        """
        ## Add a command to the register, just enter its name and the function which will be called.

        ### Posible errors:
        * Invalid Command Name
        * Invalid Command Function

        ### Example of function:
        ```
        def HelpCommand(args: list[str]) -> int:
            print("This is example of help command function.")
            return 0    # 0 - success | -1 - failed
        ```
        """
        for command in self.commands:
            if command.name == name:
                if self.print_errors: PrintError(InvalidCommandName(name, "This name is already taken"))
                return -1
            
        if not check_command_func(func):
            if self.print_errors: PrintError(InvalidCommandFunction(name, "Look on example of function in AddCommand description"))
            return -1
        
        newCommand = CommandBase(name, func)
        self.commands.append(newCommand)
        return 0

    def DeleteCommand(self, name: str) -> int:
        """
        ## Delete a command from register.

        ### Posible errors:
        * Invalid Command Name
        """
        index = 0
        for command in self.commands:
            if command.name == name:
                self.commands.pop(index)
                return 0
            index += 1
            
        if self.print_errors: PrintError(InvalidCommandName(name, "Cannot delete command because that name does not exist"))
        return -1
    
    def HandleCommand(self, command: str, args: list[str]=[]) -> int:
        """
        ## Handle command from user.

        ### Posible errors:
        * Invalid Command
        """
        for cmd in self.commands:
            if cmd.name == command:
                cmd.Run(args)
                return 0
        
        if self.print_errors: PrintError(InvalidCommand(command, "That command does not exist"))
        return -1
    
    def HandleInput(self, entry: str="") -> int:
        """
        ## Handle the entire input from user.

        ### Posible errors:
        * Invalid Command
        """
        words = entry.split()
        cmd = ""
        args = []
        if len(words) > 0: cmd = words[0]
        if len(words) > 1: args = words[1:]

        return self.HandleCommand(cmd, args)

    def __repr__(self) -> str:
        return f"CommandRegister: {len(self.commands)} commands"