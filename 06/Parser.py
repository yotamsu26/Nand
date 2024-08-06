"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.__current_line = -1
        self.__current_command = ''

        # Read lines from input file
        self.__input_lines = input_file.read().splitlines()

        # Remove start and end whitespaces from each line
        self.__input_lines = [line.strip() for line in self.__input_lines]

        # Remove \n from each line
        self.__input_lines = [line.replace('\n', '') for line in self.__input_lines]

        # Remove empty lines
        self.__input_lines = [line for line in self.__input_lines if line]

        # Remove lines starting with '/'
        self.__input_lines = [line for line in self.__input_lines if not(line.startswith('/'))]

        # Remove comments after valid lines
        self.__input_lines = [line.split('/')[0] for line in self.__input_lines]


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.__current_line < len(self.__input_lines) - 1

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.__current_line += 1
        self.__current_command = self.__input_lines[self.__current_line]

    def reset_parser(self) -> None:
        '''Resets the parser to the beginning of the input.'''
        self.__current_line = -1
        self.__current_command = ''

    
    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        self.__current_command = self.__current_command.replace(" ", "").replace("\t", "")
        if self.__current_command.startswith("(") :
            return 'L_COMMAND'
        elif self.__current_command.startswith("@"):
            return 'A_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.__current_command.startswith("(") :
            symbol = self.__current_command.split(')')[0]
            return symbol[1:]
        elif self.__current_command.startswith("@"):
            symbol = self.__current_command[1:]
            return symbol
    
    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if "=" in self.__current_command :
            parse_command = self.__current_command.split('=')
            return parse_command[0]
        else :
            return 'null'

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        comp = self.__current_command

        if "=" in self.__current_command :
            parse_command = self.__current_command.split('=')
            if ";" in parse_command[1] :
                parse_command = parse_command[1].split(';')
                comp = parse_command[0]
            else :
                comp = parse_command[1]
        elif ";" in self.__current_command :
            parse_command = self.__current_command.split(';')
            comp = parse_command[0]
        
        return comp


    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        jump = 'null'

        if "=" in self.__current_command :
            parse_command = self.__current_command.split('=')
            if ";" in parse_command[1] :
                parse_command = parse_command[1].split(';')
                if parse_command[1] != "" :
                    jump = parse_command[1]
        elif  ";" in self.__current_command :
            parse_command = self.__current_command.split(';')
            if parse_command[1] != "" :
                    jump = parse_command[1]
        
        return jump