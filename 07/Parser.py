"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
  """
  # Parser
  
  Handles the parsing of a single .vm file, and encapsulates access to the
  input code. It reads VM commands, parses them, and provides convenient 
  access to their components. 
  In addition, it removes all white space and comments.

  ## VM Language Specification

  A .vm file is a stream of characters. If the file represents a
  valid program, it can be translated into a stream of valid assembly 
  commands. VM commands may be separated by an arbitrary number of whitespace
  characters and comments, which are ignored. Comments begin with "//" and
  last until the line's end.
  The different parts of each VM command may also be separated by an arbitrary
  number of non-newline whitespace characters.

  - Arithmetic commands:
    - add, sub, and, or, eq, gt, lt
    - neg, not, shiftleft, shiftright
  - Memory segment manipulation:
    - push <segment> <number>
    - pop <segment that is not constant> <number>
    - <segment> can be any of: argument, local, static, constant, this, that, 
                                pointer, temp
  - Branching (only relevant for project 8):
    - label <label-name>
    - if-goto <label-name>
    - goto <label-name>
    - <label-name> can be any combination of non-whitespace characters.
  - Functions (only relevant for project 8):
    - call <function-name> <n-args>
    - function <function-name> <n-vars>
    - return
  """

  #### Constants ####

  # types
  POP = "pop"
  PUSH = "push"
  ARITMETIC_COMMAND_LIST = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'shiftleft', 'shiftright']

  # command types
  C_ARITHMETIC = "C_ARITHMETIC"
  C_PUSH = "C_PUSH"
  C_POP = "C_POP"

  def __init__(self, input_file: typing.TextIO) -> None:
    """Gets ready to parse the input file.

    Args:
        input_file (typing.TextIO): input file.
    """
    self.__file = input_file
    self.__current_line = -1
    self.__current_command = ''

    # Read lines from input file
    self.__input_lines = self.__file.read().splitlines()

    # Remove start and end whitespaces from each line
    self.__input_lines = [line.strip() for line in self.__input_lines]

    # Remove tabs
    self.__input_lines = [line.replace('\t', '') for line in self.__input_lines]

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
    """Reads the next command from the input and makes it the current 
    command. Should be called only if has_more_commands() is true. Initially
    there is no current command.
    """
    self.__current_line += 1
    self.__current_command = self.__input_lines[self.__current_line]

  def command_type(self) -> str:
    """
    Returns:
        str: the type of the current VM command.
        "C_ARITHMETIC" is returned for all arithmetic commands.
        For other commands, can return:
        "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
        "C_RETURN", "C_CALL".
    """
    command = self.__current_command.split(' ')[0]
    if command in Parser.ARITMETIC_COMMAND_LIST:
      return Parser.C_ARITHMETIC
    elif command == Parser.POP:
      return Parser.C_POP
    elif command == Parser.PUSH:
      return Parser.C_PUSH

  def arg1(self) -> str:
    """
    Returns:
        str: the first argument of the current command. In case of 
        "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
        Should not be called if the current command is "C_RETURN".
    """
    if self.command_type() == "C_ARITHMETIC":
      return self.__current_command.split(' ')[0]
    else: 
      return self.__current_command.split(' ')[1]

  def arg2(self) -> int:
    """
    Returns:
        int: the second argument of the current command. Should be
        called only if the current command is "C_PUSH", "C_POP", 
        "C_FUNCTION" or "C_CALL".
    """
    return int(self.__current_command.split(' ')[2])