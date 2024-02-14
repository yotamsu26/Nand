"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    # Constants

    OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    KEYWORD_CONSTANT = ["true", "false", "null", "this"]

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self._output_stream = output_stream
        self._tokenizer = input_stream
        self._prefix = ""

    def _compile_type(self) -> None:
        """Compiles a type."""
        if self._tokenizer.tokenType() == "KEYWORD" and self._tokenizer.keyWord() in ["int", "char", "boolean"]:
            self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        else:
            self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())

    def _compile_subroutine_body(self) -> None:
        self._output_stream.write(self._prefix + "<subroutineBody>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        while self._tokenizer.tokenType() == "KEYWORD" and self._tokenizer.keyWord() == "var":
            self.compile_var_dec()
        self.compile_statements()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</subroutineBody>\n")

    def _compile_subroutine_call(self, symbol: str) -> None:
        """Compiles a subroutine call."""
        if symbol == ".":
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
            self.compile_expression_list()
        else:
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self.compile_expression_list()
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._output_stream.write("<class>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # class variables declarations
        while self._tokenizer.tokenType() == "KEYWORD" and self._tokenizer.keyWord() in ["static", "field"]:
            self.compile_class_var_dec()

        # subroutines declarations
        while self._tokenizer.tokenType() == "KEYWORD" and self._tokenizer.keyWord() in ["constructor", "function", "method"]:
            self.compile_subroutine()

        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self._output_stream.write(self._prefix + "<classVarDec>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        self._compile_type()
        self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
        while self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() == ",":
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</classVarDec>\n")
        

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self._output_stream.write(self._prefix + "<subroutineDec>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        
        if self._tokenizer.tokenType() == "KEYWORD" and self._tokenizer.keyWord() == "void":
            self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        else:
            self._compile_type()

        self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self.compile_parameter_list()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self._compile_subroutine_body()

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</subroutineDec>\n")
        
        

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self._output_stream.write(self._prefix + "<parameterList>\n")

        # indentation
        self._prefix += "  "

        if self._compile_type() == True:
            self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
            while self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() == ",":
                self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
                self._compile_type()
                self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</parameterList>\n")


    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self._output_stream.write(self._prefix + "<varDec>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        self._compile_type()
        self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
        while self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() == ",": 
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self._output_stream.write(self._prefix + "<statements>\n")

        # indentation
        self._prefix += "  "

        while self._tokenizer.tokenType() == "KEYWORD" and self._tokenizer.keyWord() in ["let", "if", "while", "do", "return"]:
            if self._tokenizer.keyWord() == "let":
                self.compile_let()
            elif self._tokenizer.keyWord() == "if":
                self.compile_if()
            elif self._tokenizer.keyWord() == "while":
                self.compile_while()
            elif self._tokenizer.keyWord() == "do":
                self.compile_do()
            elif self._tokenizer.keyWord() == "return":
                self.compile_return()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._output_stream.write("<doStatement>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        self.compile_subroutine()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self._output_stream.write(self._prefix + "<letStatement>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
        # TODO another problem with process API
        if self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() == "[":
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self.compile_expression()
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self.compile_expression()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</letStatement>\n")


    def compile_while(self) -> None:
        """Compiles a while statement."""
        self._output_stream.write(self._prefix + "<whileStatement>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self.compile_expression()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self.compile_statements()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</whileStatement>\n")


    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._output_stream.write(self._prefix + "<returnStatement>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        if self._tokenizer.tokenType() != "SYMBOL" or self._tokenizer.symbol() != ";":
            self.compile_expression()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self._output_stream.write(self._prefix + "<ifStatement>\n")

        # indentation
        self._prefix += "  "

        self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self.compile_expression()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        self.compile_statements()
        self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        if self._tokenizer.tokenType() == "KEYWORD" and self._tokenizer.keyWord() == "else":
            self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self.compile_statements()
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</ifStatement>\n")
        

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._output_stream.write(self._prefix + "<expression>\n")

        # indentation
        self._prefix += "  "

        self.compile_term()
        while self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() in CompilationEngine.OP:
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self.compile_term()
        
        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</expression>\n")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self._output_stream.write(self._prefix + "<term>\n")

        # indentation
        self._prefix += "  "

        if self._tokenizer.tokenType() == "INT_CONST":
            self._process(self._tokenizer.intVal(), self._tokenizer.tokenType())
        elif self._tokenizer.tokenType() == "STRING_CONST":
            self._process(self._tokenizer.stringVal(), self._tokenizer.tokenType())
        elif self._tokenizer.tokenType() == "KEYWORD" and \
            self._tokenizer.keyWord() in CompilationEngine.KEYWORD_CONSTANT:
            self._process(self._tokenizer.keyWord(), self._tokenizer.tokenType())
        elif self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() in ["-", "~"]:
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self.compile_term()
            # TODO : check about parenthesis
        elif self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() == "(":
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            self.compile_expression()
            self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
        elif self._tokenizer.tokenType() == "IDENTIFIER":
            self._process(self._tokenizer.identifier(), self._tokenizer.tokenType())
            if self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() == "[":
                self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
                self.compile_expression()
                self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
            elif self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() in ["(", "."]:
                self._compile_subroutine_call(self._tokenizer.symbol())

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._output_stream.write(self._prefix + "<expressionList>\n")

        # indentation
        self._prefix += "  "

        if self._tokenizer.tokenType() != "SYMBOL" or self._tokenizer.symbol() == "(":
            # TODO : check if this is the only possible symbol
            self.compile_expression()
            while self._tokenizer.tokenType() == "SYMBOL" and self._tokenizer.symbol() == ",":
                self._process(self._tokenizer.symbol(), self._tokenizer.tokenType())
                self.compile_expression()

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</expressionList>\n")

    def _process(self, token: str, wrapper: str) -> None:
        """Writes the string to the output stream."""

        self._print_xml_token(token, wrapper)

        self._tokenizer.advance()

    def _print_xml_token(self, token: str, tokenType: str) -> None:
        """Writes the token to the output stream."""
        self._output_stream.write(self._prefix + 
                                  "<" + tokenType + "> " + 
                                  token + 
                                  " </" + tokenType + ">\n")
        
    # TODO : see if nessecary to call self._tokenizer.keyWord() and self._tokenizer.tokenType() in the each process