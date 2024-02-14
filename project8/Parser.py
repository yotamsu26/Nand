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
  ARITMETIC_COMMAND_LIST = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'shiftleft', 'shiftright']
  command_types = {"pop": "C_POP", "push": "C_PUSH", "label": "C_LABEL", "goto": "C_GOTO", "if-goto": "C_IF", "function": "C_FUNCTION", "return": "C_RETURN", "call": "C_CALL"}

  # command types
  C_ARITHMETIC = "C_ARITHMETIC"

  def __init__(self, input_file: typing.TextIO) -> None:
    """Gets ready to parse the input file.

    Args:
        input_file (typing.TextIO): input file.
    """
    self.file = input_file
    self.current_line = -1
    self.current_command = ''

    # Read lines from input file
    self.input_lines = self.file.read().splitlines()

    # Remove start and end whitespaces from each line
    self.input_lines = [line.strip() for line in self.input_lines]

    # Remove tabs
    self.input_lines = [line.replace('\t', '') for line in self.input_lines]

    # Remove empty lines
    self.input_lines = [line for line in self.input_lines if line]

    # Remove lines starting with '/'
    self.input_lines = [line for line in self.input_lines if not(line.startswith('/'))]

    # Remove comments after valid lines
    self.input_lines = [line.split('/')[0] for line in self.input_lines]

  def has_more_commands(self) -> bool:
    """Are there more commands in the input?

    Returns:
        bool: True if there are more commands, False otherwise.
    """
    return self.current_line < len(self.input_lines) - 1

  def advance(self) -> None:
    """Reads the next command from the input and makes it the current 
    command. Should be called only if has_more_commands() is true. Initially
    there is no current command.
    """
    self.current_line += 1
    self.current_command = self.input_lines[self.current_line]

  def command_type(self) -> str:
    """
    Returns:
        str: the type of the current VM command.
        "C_ARITHMETIC" is returned for all arithmetic commands.
        For other commands, can return:
        "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
        "C_RETURN", "C_CALL".
    """
    command = self.current_command.split(' ')[0]
    if command in Parser.ARITMETIC_COMMAND_LIST:
      return Parser.C_ARITHMETIC
    return Parser.command_types[command]

  def arg1(self) -> str:
    """
    Returns:
        str: the first argument of the current command. In case of 
        "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
        Should not be called if the current command is "C_RETURN".
    """
    if self.command_type() == "C_ARITHMETIC":
      return self.current_command.split(' ')[0]
    else: 
      return self.current_command.split(' ')[1]

  def arg2(self) -> int:
    """
    Returns:
        int: the second argument of the current command. Should be
        called only if the current command is "C_PUSH", "C_POP", 
        "C_FUNCTION" or "C_CALL".
    """
    return int(self.current_command.split(' ')[2])