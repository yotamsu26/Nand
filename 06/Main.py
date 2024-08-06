"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code
import plotly.graph_objs as go
##### constants #####

# address constants
FREE_ADDRESS_INDICATION = -1

# command types constants
A_COMMAND = 'A_COMMAND'
C_COMMAND = 'C_COMMAND'
L_COMMAND = 'L_COMMAND'

# string constants
NEW_LINE = '\n'

def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    parser = Parser(input_file)
    code = Code()
    symbol_table = SymbolTable()

    first_pass(parser, symbol_table)

    parser.reset_parser()

    second_pass(parser, code, symbol_table, output_file)


def first_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    line_counter = 0
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type==A_COMMAND or command_type==C_COMMAND:
            line_counter += 1
        elif command_type==L_COMMAND:
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, line_counter)
        

def second_pass(parser: Parser,
                 code: Code,
                   symbol_table: SymbolTable,
                     output_file: typing.TextIO) -> None:
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == A_COMMAND:
            symbol = parser.symbol()
            if not symbol.isdigit() and not symbol_table.contains(symbol):
                symbol_table.add_entry(symbol, FREE_ADDRESS_INDICATION)
            output_file.write(code.A_command(symbol, symbol_table) + NEW_LINE)
        elif command_type==C_COMMAND:
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            if "<<" in comp or ">>" in comp:
                output_file.write(code.shift_commad(dest, comp, jump) + NEW_LINE)
            else:
                output_file.write(code.C_command(dest, comp, jump) + NEW_LINE)


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    x = [3, 1.5, 0.75, 0.375, 0.1875, 0.09375, 0.046875, 0.023438, 0.011719, 0.0058594, 0.0029297, 0.001465]
    y = [2.167, 2.241, 2.078, 1.896, 1.694, 0.65, 0.465, 0.267, 0.1225, 0.051, 0.0205, 0.0335]

    # Create scatter plot
    plt.scatter(x, y)

    # Add labels and title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot')

    # Show plot
    plt.show()
