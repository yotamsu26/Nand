"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

class Code:
    """Translates Hack assembly language mnemonics into binary codes."""

    __comp_table = {"0":"0101010","1":"0111111","-1":"0111010",
                       "D":"0001100","A":"0110000","!D":"0001101",
                       "!A":"0110001","-D":"0001111","-A":"0110011",
                       "D+1":"0011111","A+1":"0110111",
                       "D-1":"0001110","A-1":"0110010",
                       "D+A":"0000010","D-A":"0010011",
                       "A-D":"0000111","D&A":"0000000",
                       "D|A":"0010101","M":"1110000",
                       "!M":"1110001","-M":"1110011",
                       "M+1":"1110111","M-1":"1110010",
                       "D+M":"1000010","D-M":"1010011",
                       "M-D":"1000111","D&M":"1000000","D|M":"1010101",  
                       "D<<": "0110000", "A<<": "0100000",
                  "M<<": "1100000", "D>>": "0010000", "A>>": "0000000",
                  "M>>": "1000000"}
    __jump_table= {"null":"000","JGT":"001","JEQ":"010",
                      "JGE":"011","JLT":"100","JNE":"101",
                      "JLE":"110","JMP":"111"}
    __dest_table = {"null":"000","M":"001","D":"010",
                       "MD":"011","A":"100","AM":"101",
                       "AD":"110","AMD":"111"}

    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        return Code.__dest_table[mnemonic]


    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        return Code.__comp_table[mnemonic]

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        return Code.__jump_table[mnemonic]


    def close(self) -> None:
        '''Closes the output file.'''
        self.output_file.close()

    def A_command(self, symbol, symbol_table) -> str:
        '''translate the A instruction into binary code'''
        if symbol.isdigit():
            return ("0" + format(int(symbol), "015b"))
        else:
            return ("0" + format(int(symbol_table.get_address(symbol)), "015b"))
            
    def C_command(self, dest, comp, jump) -> str:
        '''translate the C instruction into binary code'''
        dest = Code.dest(dest)
        comp = Code.comp(comp)
        jump = Code.jump(jump)
        return ("111" + comp + dest + jump)
    
    def shift_commad(self, dest, comp, jump) -> str:
        '''translate the shift instruction into binary code'''
        dest = Code.dest(dest)
        comp = Code.comp(comp)
        jump = Code.jump(jump)
        return ("101" + comp + dest + jump)
