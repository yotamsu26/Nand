"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
      
class CodeWriter:
  """Translates VM commands into Hack assembly code."""

  #### Constants ####

  # asm constants
  POP_SP_ASM = "@SP\n" \
                "M=M-1\n" \
                "A=M\n" \
                "D=M\n" \
                "@R13\n" \
                "A=M\n" \
                "M=D\n" 
  
  POP_REG_ASM = "// pop {0} {1}\n"\
                      "@{1}\n" \
                      "D=A\n" \
                      "@{2}\n" \
                      "D=D+M\n" \
                      "@R13\n" \
                      "M=D\n" + \
                      POP_SP_ASM

  POP_TEMP_ASM = "// pop temp {0}\n"\
                      "@{0}\n" \
                      "D=A\n" \
                      "@{1}\n" \
                      "D=D+A\n" \
                      "@R13\n" \
                      "M=D\n" +\
                      POP_SP_ASM

  POP_STATIC = "// pop static\n"\
                  "@SP\n" \
                  "M=M-1\n" \
                  "A=M\n" \
                  "D=M\n" \
                  "@{0}\n" \
                  "M=D\n"
  
  POP_POINTER = "// pop pointer {0}\n"\
                  "@{0}\n" \
                  "D=A\n" \
                  "@{1}\n" \
                  "D=D+A\n" \
                  "@R13\n" \
                  "M=D\n" +\
                  POP_SP_ASM
                  
                
  PUSH_SP_ASM = "@SP\n" \
                "M=M+1\n" \
                "A=M-1\n" \
                "M=D\n"
  
  PUSH_STATIC_ASM = "// push static {0}\n"\
                  "@{1}\n" \
                  "D=M\n" +\
                  PUSH_SP_ASM
  
  
  PUSH_POINTER_ASM = "// push pointer {0}\n"\
                  "@{0}\n" \
                  "D=A\n" \
                  "@{1}\n" \
                  "A=A+D\n" \
                  "D=M\n" +\
                  PUSH_SP_ASM
  

  CONST_PUSH_ASM = "// push const {0}\n" \
                  "@{0}\n" \
                  "D=A\n" +\
                  PUSH_SP_ASM

  PUSH_TEMP_ASM = "// push temp {0}\n" \
                  "@{0}\n" \
                  "D=A\n" \
                  "@{1}\n" \
                  "A=A+D\n" \
                  "D=M\n" +\
                  PUSH_SP_ASM

  PUSH_REG_ASM = "// push {0} {1}\n" \
                  "@{1}\n" \
                  "D=A\n" \
                  "@{2}\n" \
                  "D=D+M\n" \
                  "A=D\n" \
                  "D=M\n" +\
                  PUSH_SP_ASM

  COMPARE_ASM = "// {0} operation\n" \
              "@SP\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@R13\n" \
              "M=D\n" \
              "@Y_NEGATIVE" + "{1}\n" \
              "D;JLT\n" \
              "@SP\n" \
              "A=M-1\n" \
              "D=M\n" \
              "@X_NEGATIVE" + "{1}\n" \
              "D;JLT\n" \
              "@R13\n" \
              "D=D-M\n" \
              "@INSERT" + "{1}\n" \
              "0;JMP\n" \
              "(Y_NEGATIVE" + "{1})\n" \
              "@SP\n" \
              "A=M-1\n" \
              "D=M\n" \
              "@Y_X_NEGATIVE" + "{1}\n" \
              "D;JLT\n" \
              "D=1\n" \
              "@INSERT" + "{1}\n" \
              "0;JMP\n" \
              "(X_NEGATIVE" + "{1})\n" \
              "D = -1\n"\
              "@INSERT" + "{1}\n" \
              "0;JMP\n" \
              "(Y_X_NEGATIVE" + "{1})\n" \
              "@R13\n" \
              "D=D-M\n" \
              "@INSERT" + "{1}\n" \
              "0;JMP\n" \
              "(INSERT" + "{1})\n" \
              "@INESRT_TRUE" + "{1}\n" \
              "D;{2}\n" \
              "@SP\n" \
              "A=M-1\n" \
              "M=0\n" \
              "@CONTINUE" + "{1}\n" \
              "0;JMP\n" \
              "(INESRT_TRUE" + "{1})\n" \
              "@SP\n" \
              "A=M-1\n" \
              "M=-1\n" \
              "(CONTINUE" + "{1})\n"

  BIT_OP_ASM = "// {0} operation\n" \
      "@SP\n" \
      "M=M-1\n"\
      "A=M\n" \
      "D=M\n" \
      "A=A-1\n" \
      "M=M{1}D\n" 

  UNARY_OP = "// {0} operation\n" \
      "@SP\n" \
      "A=M-1\n" \
      "M={1}\n"
  
  INIT_ASM = "// bootstrap\n" \
      "@256\n" \
      "D=A\n" \
      "@SP\n" \
      "M=D\n" \

  
  FUNC_LABEL_ASM = " // label {1}\n" \
      "({0}${1})\n"
  
  LABEL_ASM = " // label {0}\n" \
      "({0})\n"
  
  GOTO_ASM = "// goto {0}\n" \
      "@{0}${1}\n" \
      "0;JMP\n"
  
  IF_GOTO_ASM = "// if-goto {0}${1}\n" \
      "@SP\n" \
      "M=M-1\n" \
      "A=M\n" \
      "D=M\n" \
      "@{0}${1}\n" \
      "D;JNE\n"
  
  RET_AND_LCL_ADDRESS_ASM = "// return\n" \
      "@LCL\n" \
      "D=M\n" \
      "@R14\n" \
      "M=D\n" \
      "@5\n" \
      "D=D-A\n" \
      "A=D\n" \
      "D=M\n" \
      "@R15\n" \
      "M=D\n"
  
  END_FRAME_ASM = "// endFrame {1}\n" \
      "@R14\n" \
      "D=M\n" \
      "@{0}\n" \
      "D=D-A\n" \
      "A=D\n" \
      "D=M\n" \
      "@{1}\n" \
      "M=D\n"
      
  SP_TO_ARG_PLUS_1_ASM = "@ARG\n" \
      "D=M\n" \
      "D=D+1\n" \
      "@SP\n" \
      "M=D\n"

  FUNCTION_LABEL = "// write function {0}\n" \
      "({0})\n"
  
  RETURN_ASM = "// return\n" \
      "@R15\n" \
      "A=M\n" \
      "0;JMP\n"

  #USAGE: 1 -> return label
  PUSH_RETURN_LABEL = "// push return label\n" \
    "@{0}\n" \
      "D=A\n" +\
      PUSH_SP_ASM

  ##USAGE: 1 -> name of the field (LCL, THIS ..)
  PUSH_ENV_FIELD = "// push {0}\n" \
      "@{0}\n" \
      "D=M\n" +\
      PUSH_SP_ASM

  #USAGE: 1 -> number of arguments callee except to get
  SET_NEW_ARG = "// ARG = SP-5-n_args\n" \
      "@SP\n" \
      "D=M\n" \
      "@{0}\n" \
      "D=D-A\n" \
      "@ARG\n" \
      "M=D\n"

  SET_LCL_EQ_SP = "// set LCL to be equal to SP\n" \
      "@SP\n" \
      "D=M\n" \
      "@LCL\n" \
      "M=D\n"

  #USAGE: 1 -> file name, 2 -> function name
  JUMP_TO_FUNC = "// jump to func\n" \
      "@{0}\n" \
      "0;JMP\n"

  #USAGE: 1 -> caller name, 2 -> filename, 3 -> label counter
  GENERATE_RETURN_LABEL = "{0}$ret.{1}"
  comp_op, function_counter = 0, 0

  def __init__(self, output_file: typing.TextIO) -> None:
    """Initializes the CodeWriter.

    Args:
          output_stream (typing.TextIO): output stream.
    """
    self.__output_file = output_file
    self.__file_name, self.__current_function = "", ''
    self.__segment_dic = {"local": "LCL", "argument": "ARG", "this": "THIS",
                  "that": "THAT", "temp": 5, "pointer": 3, "static": 16}
    #self.comp_op = 0
    # in order to write function label (e.g. foo$bar), this var store the current method
    self.__command_functions = {
    "add": lambda: self.__bit_op("add", "+"),
    "sub": lambda: self.__bit_op("sub", "-"),
    "eq": lambda: self.__cmp_op("eq"),
    "lt": lambda: self.__cmp_op("lt"),
    "gt": lambda: self.__cmp_op("gt"),
    "neg": lambda: self.__unary_op("neg", "-"),
    "shiftright": lambda: self.__unary_op("shiftright", ">>"),
    "shiftleft": lambda: self.__unary_op("shiftleft", "<<"),
    "and": lambda: self.__bit_op("and", "&"),
    "or": lambda: self.__bit_op("or", "|"),
    "not": lambda: self.__unary_op("not", "!"),
    }

  def bootstrap(self) -> None:
    """Writes the assembly code that is the translation of the bootstrap code."""
    self.__output_file.write(CodeWriter.INIT_ASM)
    self.write_call(function_name="Sys.init", n_args=0)


  def set_file_name(self, filename: str) -> None:
    """Informs the code writer that the translation of a new VM file is 
    started.

    Args:
        filename (str): The name of the VM file.
    """
    self.__file_name = filename


  def write_arithmetic(self, command: str) -> None:
    """Writes assembly code that is the translation of the given 
    arithmetic command. For the commands eq, lt, gt, you should correctly
    compare between all numbers our computer supports, and we define the
    value "true" to be -1, and "false" to be 0.

    Args:
        command (str): an arithmetic command.
    """
    if command in self.__command_functions:
      self.__command_functions[command]()

  def __unary_op(self, command: str, unary_op: str) -> None:
    """Writes the assembly code that is the translation of the given unary operation command."""
    if unary_op in ["<<", ">>"]:
      self.__output_file.write(CodeWriter.UNARY_OP.format(command, "M" + unary_op))
    else:
      self.__output_file.write(CodeWriter.UNARY_OP.format(command, unary_op + "M"))

  def __bit_op(self, command: str, bit_op: str) -> None:
    """Writes the assembly code that is the translation of the given bit operation command."""
    assembly_bit_op = CodeWriter.BIT_OP_ASM.format(command, bit_op)

    self.__output_file.write(assembly_bit_op)

  def __cmp_op(self, command: str) -> None:
    '''Writes the assembly code that is the translation of the gt arithmetic command.'''
    asm_command = "J" + command.upper()
    assembly_gt = CodeWriter.COMPARE_ASM.format(command, CodeWriter.comp_op, asm_command)
    CodeWriter.comp_op += 1

    self.__output_file.write(assembly_gt)

  def write_push_pop(self, command: str, segment: str, index: int) -> None:
    """Writes assembly code that is the translation of the given 
    command, where command is either C_PUSH or C_POP.

    Args:
        command (str): "C_PUSH" or "C_POP".
        segment (str): the memory segment to operate on.
        index (int): the index in the memory segment.
    """
    
    if command == "C_PUSH":
      self.__write_push(segment, index)
    elif command == "C_POP":
      self.__write_pop(segment, index)

  def __write_pop(self, segment: str, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command, where command is pop'''
    if segment == "temp":
      self.__temp_pop(index)
    elif segment == "static":
      self.__static_pop(index)
    elif segment == "pointer":
      self.__pointer_pop(index)
    else:
      self.__reg_pop(segment, index)
      
  def __write_push(self, segment: str, index: int) -> None:
      '''Writes the assembly code that is the translation of the given command, where command is push'''
      if segment == "constant":
        self.__constant_push(index)
      elif segment == "temp" :
        self.__temp_push(index)
      elif segment == "static":
        self.__static_push(index)
      elif segment == "pointer":
        self.__pointer_push( index)
      else:
        self.__reg_push(segment, index)

  def __pointer_push(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command, where command is
      C_PUSH and segment is pointer'''
    assembly_pointer_push = CodeWriter.PUSH_POINTER_ASM.format(index, self.__segment_dic["pointer"])

    self.__output_file.write(assembly_pointer_push)

  def __pointer_pop(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command, where command is
      C_POP and segment is pointer'''
    assembly_pointer_pop = CodeWriter.POP_POINTER.format(index, self.__segment_dic["pointer"])

    self.__output_file.write(assembly_pointer_pop)

  def __static_push(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command, where command is
      C_PUSH and segment is static or pointer'''
    addr = f"{self.__file_name}.{index}"
    
    assembly_static_push = CodeWriter.PUSH_STATIC_ASM.format(index, addr)

    self.__output_file.write(assembly_static_push)
    
  def __static_pop(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_POP and segment is pointer or static'''
    addr = f"{self.__file_name}.{index}"

    assembly_static_pop = CodeWriter.POP_STATIC.format(addr)

    self.__output_file.write(assembly_static_pop)

  def __temp_push(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_PUSH and segment is temp'''
    assembly_temp_push = CodeWriter.PUSH_TEMP_ASM.format(index, self.__segment_dic["temp"])

    self.__output_file.write(assembly_temp_push)

  def __temp_pop(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_POP and segment is temp'''
    assembly_temp_pop = CodeWriter.POP_TEMP_ASM.format(index, self.__segment_dic["temp"])

    self.__output_file.write(assembly_temp_pop)

  def __constant_push(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_PUSH and segment is constant'''
    assembly_constant_push = CodeWriter.CONST_PUSH_ASM.format(index)
    self.__output_file.write(assembly_constant_push)

  def __reg_push(self, segment: str, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_PUSH'''
    assembly_push = CodeWriter.PUSH_REG_ASM.format(segment,
                                                index,
                                                self.__segment_dic[segment])

    self.__output_file.write(assembly_push)

  def __reg_pop(self, segment: str, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_POP'''
    assembly_pop = CodeWriter.POP_REG_ASM.format(segment, index,
                                              self.__segment_dic[segment])

    self.__output_file.write(assembly_pop)

  def write_label(self, label: str) -> None:
    """Writes assembly code that affects the label command. 
    Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
    each "label bar" command within "Xxx.foo" generates and injects the symbol
    "Xxx.foo$bar" into the assembly code stream.
    When translating "goto bar" and "if-goto bar" commands within "foo",
    the label "Xxx.foo$bar" must be used instead of "bar".

    Args:
        label (str): the label to write.
    """
    self.__output_file.write(CodeWriter.FUNC_LABEL_ASM.format(self.__current_function, label))

  def write_goto(self, label: str) -> None:
    """Writes assembly code that affects the goto command.

    Args:
        label (str): the label to go to.
    """
    assembly_goto = CodeWriter.GOTO_ASM.format(self.__current_function, label)

    self.__output_file.write(assembly_goto)

  def write_if(self, label: str) -> None:
    """Writes assembly code that affects the if-goto command. 

    Args:
        label (str): the label to go to.
    """
    assembly_if = CodeWriter.IF_GOTO_ASM.format(self.__current_function, label)

    self.__output_file.write(assembly_if)

  def write_function(self, function_name: str, n_vars: int) -> None:
    """Writes assembly code that affects the function command. 
    The handling of each "function Xxx.foo" command within the file Xxx.vm
    generates and injects a symbol "Xxx.foo" into the assembly code stream,
    that labels the entry-point to the function's code.
    In the subsequent assembly process, the assembler translates this 
    symbol into the physical address where the function code starts.

    Args:
        function_name (str): the name of the function.
        n_vars (int): the number of local variables of the function.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    # The pseudo-code of "function function_name n_vars" is:
    # (function_name)       // injects a function entry label into the code
    # repeat n_vars times:  // n_vars = number of local variables
    #   push constant 0     // initializes the local variables to 0
    self.__current_function = function_name
    self.__output_file.write(CodeWriter.FUNCTION_LABEL.format(function_name))
    for i in range(n_vars):
        self.__constant_push(0)

  def write_call(self, function_name: str, n_args: int) -> None:
    """Writes assembly code that affects the call command. 
    Let "Xxx.foo" be a function within the file Xxx.vm.
    The handling of each "call" command within Xxx.foo's code generates and
    injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
    "i" is a running integer (one such symbol is generated for each "call"
    command within "Xxx.foo").
    This symbol is used to mark the return address within the caller's 
    code. In the subsequent assembly process, the assembler translates this
    symbol into the physical memory address of the command immediately
    following the "call" command.

    Args:
        function_name (str): the name of the function to call.
        n_args (int): the number of arguments of the function.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    # The pseudo-code of "call function_name n_args" is:
    # push return_address   // generates a label and pushes it to the stack

    CodeWriter.function_counter += 1
    return_address = CodeWriter.GENERATE_RETURN_LABEL.format(self.__current_function, CodeWriter.function_counter)
    command = CodeWriter.PUSH_RETURN_LABEL.format(return_address)
    # push LCL              // saves LCL of the caller
    command += CodeWriter.PUSH_ENV_FIELD.format("LCL")
    # push ARG              // saves ARG of the caller
    command += CodeWriter.PUSH_ENV_FIELD.format("ARG")
    # push THIS             // saves THIS of the caller
    command += CodeWriter.PUSH_ENV_FIELD.format("THIS")
    # push THAT             // saves THAT of the caller
    command += CodeWriter.PUSH_ENV_FIELD.format("THAT")
    # ARG = SP-5-n_args     // repositions ARG
    command += CodeWriter.SET_NEW_ARG.format(f"{int(n_args) + 5}")
    # LCL = SP              // repositions LCL
    command += CodeWriter.SET_LCL_EQ_SP
    # goto function_name    // transfers control to the callee
    command += CodeWriter.JUMP_TO_FUNC.format(f"{function_name}")
    # (return_address)      // injects the return address label into the code
    command += "(" + return_address + ")\n"

    self.__output_file.write(command)

  def write_return(self) -> None:
    """Writes assembly code that affects the return command."""
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    # The pseudo-code of "return" is:
    # frame = LCL                   // frame is a temporary variable
    # return_address = *(frame-5)   // puts the return address in a temp var
    # *ARG = pop()                  // repositions the return value for the caller
    # SP = ARG + 1                  // repositions SP for the caller
    # THAT = *(frame-1)             // restores THAT for the caller
    # THIS = *(frame-2)             // restores THIS for the caller
    # ARG = *(frame-3)              // restores ARG for the caller
    # LCL = *(frame-4)              // restores LCL for the caller
    # goto return_address           // go to the return address

    # frame = LCL, return_address = *(frame-5)
    self.__output_file.write(CodeWriter.RET_AND_LCL_ADDRESS_ASM.format())
    # *ARG = pop()
    self.__reg_pop("argument", 0)
    # SP = ARG + 1
    command = CodeWriter.SP_TO_ARG_PLUS_1_ASM.format()
    # THAT = *(frame-1)
    command += CodeWriter.END_FRAME_ASM.format(1, "THAT")
    # THIS = *(frame-2)
    command += CodeWriter.END_FRAME_ASM.format(2, "THIS")
    # ARG = *(frame-3)
    command += CodeWriter.END_FRAME_ASM.format(3, "ARG")
    # LCL = *(frame-4)
    command += CodeWriter.END_FRAME_ASM.format(4, "LCL")
    # goto return_address
    command += CodeWriter.RETURN_ASM

    self.__output_file.write(command)


    
