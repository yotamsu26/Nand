"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import JackTokenizer
from JackTokenizer import KEYWORD, IDENTIFIER, SYMBOL, INT_CONST, STRING_CONST



class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    # Constants

    OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    KEYWORD_CONSTANT = ["true", "false", "null", "this"]
    OP_DEC = {"<" : "&lt;", ">" : "&gt;", "&" : "&amp;"}

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
        if self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() in \
                ["int", "char", "boolean"]:
            self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # the type is a class name which is identifier
        else:
            self._process(self._tokenizer.identifier(), self._tokenizer.token_type())

    def _compile_subroutine_body(self) -> None:
        """Compiles a subroutine body."""
        # xml tag
        self._output_stream.write(self._prefix + "<subroutineBody>\n")

        # indentation
        self._prefix += "  "

        # process '{' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # var declarations
        while self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() == "var":
            self.compile_var_dec()
        # statements    
        self.compile_statements()
        # process '}' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]

        # xml tag
        self._output_stream.write(self._prefix + "</subroutineBody>\n")

    def _compile_subroutine_call(self, symbol: str) -> None:
        """Compiles a subroutine call."""
        # process subroutine name
        if symbol == ".":
            while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ".":
                self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
                self._process(self._tokenizer.identifier(), self._tokenizer.token_type())

        # process '(' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process expression list
        self.compile_expression_list()
        # process ')' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # xml tag
        self._output_stream.write("<class>\n")

        # indentation
        self._prefix += "  "

        # process class keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process class name which is identifier
        self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
        # process '{' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # class variables declarations
        while self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() in \
                ["static", "field"]:
            self.compile_class_var_dec()

        # subroutines declarations
        while self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() in \
                ["constructor", "function", "method"]:
            self.compile_subroutine()

        # process '}' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]

        # xml tag
        self._output_stream.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # xml tag
        self._output_stream.write(self._prefix + "<classVarDec>\n")

        # indentation
        self._prefix += "  "

        # process static or field keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process type
        self._compile_type()
        # process variable name
        self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
        # process ',' and variable names if exists
        while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ",":
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
            self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
        # process ';' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]

        # xml tag
        self._output_stream.write(self._prefix + "</classVarDec>\n")
        

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # xml tag
        self._output_stream.write(self._prefix + "<subroutineDec>\n")

        # indentation
        self._prefix += "  "

        # process constructor, function or method keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        
        # process return type
        if self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() == "void":
            self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        else:
            self._compile_type()

        # process subroutine name
        self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
        # process '(' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process parameter list
        self.compile_parameter_list()
        # process ')' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process subroutine body
        self._compile_subroutine_body()

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</subroutineDec>\n")
        
        

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # xml tag
        self._output_stream.write(self._prefix + "<parameterList>\n")

        # indentation
        self._prefix += "  "

        # if self._compile_type() == True:
        if self._tokenizer.token_type() != SYMBOL:
            self._compile_type()
            self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
            while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ",":
                self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
                self._compile_type()
                self._process(self._tokenizer.identifier(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]

        # xml tag
        self._output_stream.write(self._prefix + "</parameterList>\n")


    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # xml tag
        self._output_stream.write(self._prefix + "<varDec>\n")

        # indentation
        self._prefix += "  "
        # process var keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process type
        self._compile_type()
        # process variable name
        self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
        # process ',' and variable names if exists
        while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ",":
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
            self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
        # process ';' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # xml tag
        self._output_stream.write(self._prefix + "<statements>\n")

        # indentation
        self._prefix += "  "

        # process statements
        while self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() in \
                ["let", "if", "while", "do", "return"]:
            if self._tokenizer.keyword() == "let":
                self.compile_let()
            elif self._tokenizer.keyword() == "if":
                self.compile_if()
            elif self._tokenizer.keyword() == "while":
                self.compile_while()
            elif self._tokenizer.keyword() == "do":
                self.compile_do()
            elif self._tokenizer.keyword() == "return":
                self.compile_return()

        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # xml tag
        self._output_stream.write(self._prefix + "<doStatement>\n")

        # indentation
        self._prefix += "  "
        # process do keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type()) 
        # process subroutine name or class name or variable name
        self._process(self._tokenizer.identifier(), self._tokenizer.token_type()) 
        # process subroutine call according to the next token
        while self._tokenizer.token_type() != SYMBOL or self._tokenizer.symbol() != "(":
            if self._tokenizer.token_type == IDENTIFIER:
                self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
            else:
                self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process '(' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process expression list
        self.compile_expression_list()

        # process ')' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process ';' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]

        self._output_stream.write(self._prefix + "</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self._output_stream.write(self._prefix + "<letStatement>\n")

        # indentation
        self._prefix += "  "
        # process let keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process variable name
        self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
        # process '[' and expression if exists
        if self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == "[":
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
            self.compile_expression()
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process '=' char  
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process expression
        self.compile_expression()
        # process ';' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</letStatement>\n")


    def compile_while(self) -> None:
        """Compiles a while statement."""
        # xml tag
        self._output_stream.write(self._prefix + "<whileStatement>\n")

        # indentation
        self._prefix += "  "
        # process while keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process '(' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process expression
        self.compile_expression()
        # process ')' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process '{' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process statements
        self.compile_statements()
        # process '}' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</whileStatement>\n")


    def compile_return(self) -> None:
        """Compiles a return statement."""
        # xml tag
        self._output_stream.write(self._prefix + "<returnStatement>\n")

        # indentation
        self._prefix += "  "
        # process return keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process expression if exists
        if self._tokenizer.token_type() != SYMBOL or self._tokenizer.symbol() != ";":
            self.compile_expression()
        # process ';' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # xml tag
        self._output_stream.write(self._prefix + "<ifStatement>\n")

        # indentation
        self._prefix += "  "
        # process if keyword
        self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process '(' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process expression
        self.compile_expression()
        # process ')' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process '{' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process statements
        self.compile_statements()
        # process '}' char
        self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process else clause if exists
        if self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() == "else":
            self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
            self.compile_statements()
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())

        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</ifStatement>\n")
        

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # xml tag
        self._output_stream.write(self._prefix + "<expression>\n")

        # indentation
        self._prefix += "  "

        # process term
        self.compile_term()
        # process op and term if exists
        while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() in CompilationEngine.OP:
            val = self._tokenizer.symbol()
            if val in CompilationEngine.OP_DEC.keys():
                val = CompilationEngine.OP_DEC[val]
            self._process(val, self._tokenizer.token_type())
            self.compile_term()
        
        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
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
        # xml tag
        self._output_stream.write(self._prefix + "<term>\n")

        # indentation
        self._prefix += "  "
        # process term if INT_CONST
        if self._tokenizer.token_type() == INT_CONST:
            self._process(self._tokenizer.int_val(), self._tokenizer.token_type())
        # process term if STRING_CONST
        elif self._tokenizer.token_type() == STRING_CONST:
            self._process(self._tokenizer.string_val(), self._tokenizer.token_type())
        # process term if KEYWORD is true, false, null or this
        elif self._tokenizer.token_type() == KEYWORD and \
            self._tokenizer.keyword() in CompilationEngine.KEYWORD_CONSTANT:
            self._process(self._tokenizer.keyword(), self._tokenizer.token_type())
        # process term if SYMBOL is in ['-', '~', '#', '^']
        elif self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() in ["-", "~", "#", "^"]:
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
            self.compile_term()
        # process expression if SYMBOL is '(' 
        elif self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == "(":
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
            self.compile_expression()
            self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
        # process term if IDENTIFIER
        elif self._tokenizer.token_type() == IDENTIFIER:
            self._process(self._tokenizer.identifier(), self._tokenizer.token_type())
            if self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == "[":
                self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
                self.compile_expression()
                self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
            elif self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() in ["(", "."]:
                self._compile_subroutine_call(self._tokenizer.symbol())
        
        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</term>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # xml tag
        self._output_stream.write(self._prefix + "<expressionList>\n")

        # indentation
        self._prefix += "  "

        # process expression if exists
        if not (self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ")"):
            self.compile_expression()
            while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ",":
                self._process(self._tokenizer.symbol(), self._tokenizer.token_type())
                self.compile_expression()

        # indentation
        self._prefix = self._prefix[:-2]
        # xml tag
        self._output_stream.write(self._prefix + "</expressionList>\n")

    def _process(self, token: str, wrapper: str) -> None:
        """Writes the string to the output stream."""

        self._print_xml_token(token, wrapper)

        self._tokenizer.advance()

    def _print_xml_token(self, token: str, tokenType: str) -> None:
        """Writes the token to the output stream."""
        self._output_stream.write(self._prefix + 
                                  "<" + tokenType + "> " + 
                                  str(token) +
                                  " </" + tokenType + ">\n")
        