"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from SymbolTable import SymbolTable
from JackTokenizer import KEYWORD, IDENTIFIER, SYMBOL, INT_CONST, STRING_CONST, JackTokenizer
from VMWriter import VMWriter

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    UNARY_OP_DEC = {"-": "neg", "~": "not", "#": "rightshift", "^": "leftshift"}
    BINARY_OP_DEC = {"+": "add", "-": "sub", "*": "call Math.multiply 2", "/": "call Math.divide 2",
                     "<": "lt", ">": "gt", "=": "eq", "|": "or", "&": "and"
                     }
    SEG_MAP = {SymbolTable.ARG_KIND: "argument",
               SymbolTable.VAR_KIND: "local",
               SymbolTable.STATIC_KIND: "static",
               SymbolTable.FIELD_KIND: "this"
               }
    # this dictionary maps between keywords and their segment and index
    KEYWORD_MAP = {"true": ("constant", 0),
                   "false": ("constant", 0),
                   "null": ("constant", 0),
                   "this": ("pointer", 0)
                   }

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self._tokenizer = input_stream
        self._output = output_stream
        self._symbol_table = SymbolTable()
        self._writer = VMWriter(output_stream=output_stream)
        self._generator_label_counter = 0
        self._class_name = ''


    def compile_class(self) -> None:
        """Compiles a complete class."""
        #advance after the class
        self._tokenizer.advance()
        #advance after the class name after saving it
        self._class_name = self._tokenizer.identifier()
        self._tokenizer.advance()
        #advance after the {
        self._tokenizer.advance()
        #compile the class var dec
        while self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() in \
                ["static", "field"]:
            self.compile_class_var_dec()
        #compile the subroutine
        while self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() in \
                ["constructor", "function", "method"]:
            self.compile_subroutine()

        #advance after the }
        self._tokenizer.advance()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # save the kind
        kind = self._tokenizer.keyword()
        # as this class var we can assume its kind is either static or field
        if kind == "static":
            kind = SymbolTable.STATIC_KIND
        else: kind = SymbolTable.FIELD_KIND
        # advance after the static or field
        self._tokenizer.advance()
        # save the type
        var_type = self._compile_type()
        # advance after the type
        self._tokenizer.advance()
        # save the name 
        var_name = self._tokenizer.identifier()
        #advance after the name
        self._tokenizer.advance()
        # add to symbol_table
        self._symbol_table.define(name=var_name, type=var_type, kind=kind)
        # handle declaration in the form of static int HORZ_CAR, VERT_CAR, VERT_TRUCK, RED;
        while self._tokenizer.symbol() == ",":
            self._tokenizer.advance()
            var_name = self._tokenizer.identifier()
            self._tokenizer.advance()
            self._symbol_table.define(name=var_name, type=var_type, kind=kind)
        #advance after the ;
        self._tokenizer.advance()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        #initialize the symbol table
        self._symbol_table.start_subroutine()
        #save the subroutine type
        subroutine_type = self._tokenizer.keyword()
        #advance after the constructor, function, or method
        self._tokenizer.advance()
        #advance after the return type
        self._tokenizer.advance()
        # advance after the subroutine name after saving it
        sub_name = self._tokenizer.identifier()
        self._tokenizer.advance()
        # add this to the symbol table
        if subroutine_type == "method":
            self._symbol_table.define(name="this", type=self._class_name, kind=SymbolTable.ARG_KIND)
        #advance after the (
        self._tokenizer.advance()
        #compile the parameter list
        self.compile_parameter_list()
        #advance after the )
        self._tokenizer.advance()
        #advance after the {
        self._tokenizer.advance()
        #compile the var dec
        while self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() == "var":
            self.compile_var_dec()
        # write the function command
        s = self._symbol_table.var_count(kind=SymbolTable.VAR_KIND)
        self._writer.write_function(name=f"{self._class_name}.{sub_name}",
                                     n_locals=s)
        # handle constructor
        if subroutine_type == "constructor":
            # write the memory allocation command
            self._writer.write_push(segment="constant", index=self._symbol_table.var_count(kind=SymbolTable.FIELD_KIND))
            self._writer.write_call(name="Memory.alloc", n_args=1)
            self._writer.write_pop(segment="pointer", index=0)
        # handle method
        if subroutine_type == "method":
            self._writer.write_push(segment="argument", index=0)
            self._writer.write_pop(segment="pointer", index=0)

        #compile the statements
        self.compile_statements()
        #advance after the }
        self._tokenizer.advance()


    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # compile the type
        curType = self._compile_type()
        if curType == ')':
            return
        # advance after the type
        self._tokenizer.advance()
        # compile the var name
        varName = self._tokenizer.identifier()
        # advance after the var name
        self._tokenizer.advance()
        # add to symbol table
        self._symbol_table.define(name=varName, type=curType, kind=SymbolTable.ARG_KIND)
        # handle the case of multiple parameters
        while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ",":
            # advance after the ,
            self._tokenizer.advance()
            # compile the type
            curType = self._compile_type()
            # advance after the type
            self._tokenizer.advance()
            # compile the var name
            varName = self._tokenizer.identifier()
            # advance after the var name
            self._tokenizer.advance()
            # add to symbol table
            self._symbol_table.define(name=varName, type=curType, kind=SymbolTable.ARG_KIND)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # advance after the var
        self._tokenizer.advance()
        # compile the type
        var_type = self._compile_type()
        # advance after the type
        self._tokenizer.advance()
        # compile the var name
        var_name = self._tokenizer.identifier()
        # advance after the var name
        self._tokenizer.advance()
        # add to symbol table
        self._symbol_table.define(name=var_name, type=var_type, kind=SymbolTable.VAR_KIND)
        # handle the case of multiple variables
        while self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ",":
            # advance after the ,
            self._tokenizer.advance()
            # compile the var name
            var_name = self._tokenizer.identifier()
            # advance after the var name
            self._tokenizer.advance()
            # add to symbol table
            self._symbol_table.define(name=var_name, type=var_type, kind=SymbolTable.VAR_KIND)
        # advance after the ;
        self._tokenizer.advance()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """

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

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # advance after the do
        self._tokenizer.advance()
        # compile the expression
        self.compile_expression()
        # advance after the ;
        self._tokenizer.advance()
        # write the pop command
        self._writer.write_pop(segment="temp", index=0)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # advance after the let
        self._tokenizer.advance()
        # compile the expression
        var_name = self._tokenizer.identifier()
        if self._tokenizer.look_ahead()[1] == "[":
            #lets assume we handle a[exp_1] = exp_2
            self._writer.write_push(segment=CompilationEngine.SEG_MAP[self._symbol_table.kind_of(var_name)],
                                    index=self._symbol_table.index_of(var_name))
            self._tokenizer.advance() #got [
            self._tokenizer.advance() #got exp_1
            self.compile_expression()
            self._tokenizer.advance() #got =
            self._writer.write_arithmetic(command="add") # put a + exp_1 at the top of the stack
            self._tokenizer.advance() # got exp_2
            self.compile_expression()
            self._writer.write_pop(segment="temp", index=0)
            self._writer.write_pop(segment="pointer", index=1)
            self._writer.write_push(segment="temp", index=0)
            self._writer.write_pop(segment="that", index=0)

        else:
            self._tokenizer.advance()  # advance =
            self._tokenizer.advance()
            self.compile_expression()
            seg = CompilationEngine.SEG_MAP[self._symbol_table.kind_of(var_name)]
            index = self._symbol_table.index_of(var_name)
            self._writer.write_pop(segment=seg, index=index)  # assign the value into the variable

        # advance after the ;
        self._tokenizer.advance()

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # generate labels
        label1 = f"L.{self._generator_label_counter}"
        label2 = f"L.{self._generator_label_counter + 1}"
        self._generator_label_counter += 2

        # write the label1
        self._writer.write_label(label1)
        # advance after the while
        self._tokenizer.advance()
        # advance after the (
        self._tokenizer.advance()
        # compile the expression
        self.compile_expression()
        # advance after the )
        self._tokenizer.advance()
        # write not command
        self._writer.write_arithmetic(command="not")
        # write if-goto label2
        self._writer.write_if(label2)
        # advance after the {
        self._tokenizer.advance()
        # compile the statements
        self.compile_statements()
        # advance after the }
        self._tokenizer.advance()
        # write goto label1
        self._writer.write_goto(label1)
        # write the label2
        self._writer.write_label(label2)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # advance after the return
        self._tokenizer.advance()
        # evaluate the expression and put it on the top of the stack
        if self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ";":
            self._writer.write_push(segment=VMWriter.CONSTANT_SEG, index=0) #in case void should return
        if self._tokenizer.token_type() != SYMBOL or self._tokenizer.symbol() != ";":
            self.compile_expression()
        # write the return command 
        self._writer.write_return()
        self._tokenizer.advance() #advance after ;

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # generate labels
        label1 = f"L.{self._generator_label_counter}"
        label2 = f"L.{self._generator_label_counter + 1}"
        self._generator_label_counter += 2

        # advance after the if
        self._tokenizer.advance()
        # advance after the (
        self._tokenizer.advance()
        # compile the expression
        self.compile_expression()
        # advance after the )
        self._tokenizer.advance()
        # write not command
        self._writer.write_arithmetic(command="not")
        # write if-goto label1
        self._writer.write_if(label1)
        # advance after the {
        self._tokenizer.advance()
        # compile the statements
        self.compile_statements()
        # advance after the }
        self._tokenizer.advance()
        # write goto label2
        self._writer.write_goto(label2)
        # write the label1
        self._writer.write_label(label1)
        # if there is an else
        if self._tokenizer.token_type() == KEYWORD and self._tokenizer.keyword() == "else":
            # advance after the else
            self._tokenizer.advance()
            # advance after the {
            self._tokenizer.advance()
            # compile the statements
            self.compile_statements()
            # advance after the }
            self._tokenizer.advance()
        # write the label2
        self._writer.write_label(label2)


    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term() # assume advance the tokenizer
        while self._tokenizer.token_type() == SYMBOL and \
            self._tokenizer.symbol() in CompilationEngine.BINARY_OP_DEC.keys():
            symbol = self._tokenizer.symbol()
            self._tokenizer.advance() #pass the operator
            #compile the next term in order to operate on both
            self.compile_term() # assume advance the tokenizer
            # write the operator
            self._writer.write_arithmetic(command=CompilationEngine.BINARY_OP_DEC[symbol])


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
        if self._tokenizer.keyword() in CompilationEngine.KEYWORD_MAP.keys():
            seg, ind = CompilationEngine.KEYWORD_MAP[self._tokenizer.keyword()]
            self._writer.write_push(segment=seg, index=ind)
            if self._tokenizer.keyword() == "true":
                self._writer.write_arithmetic("not")
            self._tokenizer.advance()

        cur_type = self._tokenizer.token_type()
        if cur_type == SYMBOL and self._tokenizer.symbol() == "(":
            self._tokenizer.advance()
            self.compile_expression()
            self._tokenizer.advance() #pass )
            return

        # process const int
        if cur_type == INT_CONST:
            self._writer.write_push(segment=VMWriter.CONSTANT_SEG, index=self._tokenizer.int_val())
            self._tokenizer.advance()

        #handle string
        elif cur_type == STRING_CONST:
            self._compile_string()


        #handle unary operator
        elif cur_type == SYMBOL and self._tokenizer.symbol() in CompilationEngine.UNARY_OP_DEC.keys():
            self._handle_unary_op()

        #handle identifier
        elif cur_type == IDENTIFIER:
            self._handle_identifier_in_term()


    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        counter = 0
        self._tokenizer.advance() # pass (
        while self._tokenizer.symbol() != ')':
            counter += 1
            self.compile_expression() #assume advance
            if self._tokenizer.symbol() == ",":
                self._tokenizer.advance() #advance ,

        return counter
    
    def _compile_subroutine_call(self) -> None:
        # advance after the subroutine name or the class name after saving it
        curName = self._tokenizer.identifier()
        self._tokenizer.advance()
        
        # compile the expression list if symbol is (
        if self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == "(":
            #advance after the (
            self._tokenizer.advance()
            # compile the expression list and save the number of arguments
            nArgs = self.compile_expression_list()
            # write the call command
            self._writer.write_call(name=f"{self._class_name}.{curName}", n_args=nArgs)
            #advance after the )
            self._tokenizer.advance()
        
        # compile the expression list if symbol is .
        elif self._tokenizer.token_type() == SYMBOL and self._tokenizer.symbol() == ".":
            #advance after the .
            self._tokenizer.advance()
            #advance after the subroutine name after saving it
            curName += f".{self._tokenizer.identifier()}"
            self._tokenizer.advance()
            #advance after the (
            self._tokenizer.advance()
            # compile the expression list and save the number of arguments
            nArgs = self.compile_expression_list()
            # write the call command
            self._writer.write_call(name=curName, n_args=nArgs)
            #advance after the )
            self._tokenizer.advance()
    def _compile_string(self) -> None:
        #push string lem into the stack
        self._writer.write_push(segment=VMWriter.CONSTANT_SEG, index=len(self._tokenizer.string_val()))
        self._writer.write_call(name="String.new",n_args=1)
        for char in self._tokenizer.string_val():
            #push the car ascii value
            self._writer.write_push(segment=VMWriter.CONSTANT_SEG, index=ord(char))
            self._writer.write_call("String.appendChar", 2) #this function return the string to the top of the stack
        self._tokenizer.advance()


    def _compile_type(self) -> str:
        """Compiles a type."""
        cur_type = self._tokenizer.token_type()
        if cur_type == KEYWORD:
            return self._tokenizer.keyword()
        else:
            return self._tokenizer.identifier()

    def _handle_identifier_in_term(self):
        cur_identifier = self._tokenizer.identifier()
        is_method = False


        class_name = cur_identifier
        if self._symbol_table.kind_of(cur_identifier):  # return None if this is not exist var
            self._writer.write_push(segment=CompilationEngine.SEG_MAP[self._symbol_table.kind_of(cur_identifier)],
                                    index=self._symbol_table.index_of(cur_identifier))
            class_name = self._symbol_table.type_of(cur_identifier)
            is_method = True
        if self._tokenizer.look_ahead()[1] == "[":
            self._handle_array_in_term()
        # this look do not advance the tokenizer
        func_name = class_name
        self._tokenizer.advance()
        if self._tokenizer.symbol() == ".":  # form of var.method_name()
            self._tokenizer.advance()
            func_name += f".{self._tokenizer.identifier()}"
            self._tokenizer.advance()
        if self._tokenizer.symbol() == "(":
            # call to function
            n_args = self.compile_expression_list()
            if  is_method:
                n_args += 1
            self._writer.write_call(name=func_name, n_args=n_args)
            self._tokenizer.advance()  # get )


        #advance?


    def _handle_array_in_term(self):
        # assume the command is a[exp_1]
        self._tokenizer.advance() # got [
        self._tokenizer.advance()
        self.compile_expression() # compile exp_1
        self._writer.write_arithmetic(CompilationEngine.BINARY_OP_DEC["+"])
        #self._writer.write_pop(segment="temp", index=0)
        self._writer.write_pop(segment="pointer", index=1)
        self._writer.write_push(segment="that", index=0)
        #self._tokenizer.advance()




    def _handle_unary_op(self):
        cur_symbol = self._tokenizer.symbol()
        # push the next term
        self._tokenizer.advance()
        self.compile_term()
        self._writer.write_arithmetic(self.UNARY_OP_DEC[cur_symbol])



