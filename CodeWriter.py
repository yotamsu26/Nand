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
  
  POP_ASM = "// pop {0} {1}\n"\
                      "@{1}\n" \
                      "D=A\n" \
                      "@{2}\n" \
                      "D=D+M\n" \
                      "@R13\n" \
                      "M=D\n" + \
                      POP_SP_ASM

  POP_TEMP_ASM = "// pop {0} {1}\n"\
                      "@{1}\n" \
                      "D=A\n" \
                      "@{2}\n" \
                      "D=D+A\n" \
                      "@R13\n" \
                      "M=D\n" +\
                      POP_SP_ASM

  POP_STATIC_OR_POINTER = "// pop {0} {1}\n"\
                  "@SP\n" \
                  "M=M-1\n" \
                  "A=M\n" \
                  "D=M\n" \
                  "@{2}\n" \
                  "M=D\n"

  PUSH_POINTER_OR_STATIC_ASM = "// push {0} {1}\n"\
                  "@{2}\n" \
                  "D=M\n" \
                  "@SP\n" \
                  "A=M\n" \
                  "M=D\n" \
                  "@SP\n" \
                  "M=M+1\n"
  
  PUSH_SP_ASM = "@SP\n" \
                "M=M+1\n" \
                "A=M-1\n" \
                "M=D\n"

  CONST_PUSH_ASM = "// push {0} {1}\n" \
                  "@{1}\n" \
                  "D=A\n" +\
                  PUSH_SP_ASM

  PUSH_TEMP_ASM = "// push {0} {1}\n" \
                  "@{1}\n" \
                  "D=A\n" \
                  "@{2}\n" \
                  "D=D+A\n" \
                  "A=D\n" \
                  "D=M\n" +\
                  PUSH_SP_ASM

  PUSH_ASM = "// push {0} {1}\n" \
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
              "@INSERT" + "{1}\n" \
              "0;JMP\n" \
              "(X_NEGATIVE" + "{1})\n" \
              "D=D\n" \
              "@INSERT" + "{1}\n" \
              "0;JMP\n" \
              "(Y_X_NEGATIVE" + "{1})\n" \
              "@R13\n" \
              "D=M-D\n" \
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
      "M={1}M\n"
  
  FUNC_LABEL_ASM = " // label {1}\n" \
      "({0}${1})\n"
  
  LABEL_ASM = " // label {0}\n" \
      "({0})\n"
  
  GOTO_ASM = "// goto {0}\n" \
      "@{0}\n" \
      "0;JMP\n"
  
  IF_GOTO_ASM = "// if-goto {0}\n" \
      "@SP\n" \
      "M=M-1\n" \
      "A=M\n" \
      "D=M\n" \
      "@{0}\n" \
      "D;JGT\n" \
      "D;JLT\n"
  
  RET_AND_LCL_ADDRESS_ASM = "// return\n" \
      "@LCL\n" \
      "D=M\n" \
      "@endFrame\n" \
      "M=D\n" \
      "@5\n" \
      "D=D-A\n" \
      "@retAddr\n" \
      "M=D\n"
  
  END_FRAME_ASM = "@endFrame\n" \
      "M=D\n" \
      "@{0}\n" \
      "D=D-A\n" \
      "@{1}\n" \
      "M=D\n"
      
  SP_TO_ARG_PLUS_1_ASM = "@ARG\n" \
      "A=M\n" \
      "M=D\n" \
      "D=D+1\n" \
      "@SP\n" \
      "M=D\n"

  FUNCTION_LABEL = "// write function {1}\n" \
      "({2}.{1}"

  #USAGE: 1 -> return label
  PUSH_RETURN_LABEL = "// push return label\n" \
    "{1}\n" \
      "D=A\n" \
      "@SP\n" \
      "A=M\n" \
      "M=D\n" \
      "@SP\n" \
      "M=M+1\n"

  ##USAGE: 1 -> name of the field (LCL, THIS ..)
  PUSH_ENV_FIELD = "// push {1}\n" \
      "@{1}\n" \
      "D=M\n" \
      "@SP\n" \
      "A=M\n" \
      "M=D\n" \
      "@SP\n" \
      "M=M+1\n"

  #USAGE: 1 -> number of arguments callee except to get
  SET_NEW_ARG = "// ARG = SP-5-n_args\n" \
      "@SP\n" \
      "D=A\n" \
      "@5\n" \
      "D=D-A\n" \
      "@{1}\n" \
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
      "@{1}.{2}\n" \
      "0;JMP\n"

  #USAGE: 1 -> caller name, 2 -> filename, 3 -> label counter
  GENERATE_RETURN_LABEL = "// insert return point\n" \
      "({2}.{1}$ret.{3})\n"

  def __init__(self, output_file: typing.TextIO) -> None:
    """Initializes the CodeWriter.

    Args:
          output_stream (typing.TextIO): output stream.
    """
    self.output_file = output_file
    self.file_name, self.current_function = "", ""
    self.segment_dic = {"local": "LCL", "argument": "ARG", "this": "THIS",
                  "that": "THAT", "temp": 5, "pointer": 3, "static": 16}
    self.comp_op = 0
    # in order to write function label (e.g. foo$bar), this var store the current method
    self._cur_method = ""
    self.command_functions = {
    "add": lambda: self.write_bit_op("add", "+"),
    "sub": lambda: self.write_bit_op("sub", "-"),
    "eq": lambda: self.write_cmp("eq"),
    "lt": lambda: self.write_cmp("lt"),
    "gt": lambda: self.write_cmp("gt"),
    "neg": lambda: self.write_unary_op("neg", "-"),
    "shiftright": lambda: self.write_unary_op("shiftright", ">>"),
    "shiftleft": lambda: self.write_unary_op("shiftleft", "<<"),
    "and": lambda: self.write_bit_op("and", "&"),
    "or": lambda: self.write_bit_op("or", "|"),
    "not": lambda: self.write_unary_op("not", "!"),
    }
    

  def set_file_name(self, filename: str) -> None:
    """Informs the code writer that the translation of a new VM file is 
    started.

    Args:
        filename (str): The name of the VM file.
    """
    self.file_name = filename


  def write_arithmetic(self, command: str) -> None:
    """Writes assembly code that is the translation of the given 
    arithmetic command. For the commands eq, lt, gt, you should correctly
    compare between all numbers our computer supports, and we define the
    value "true" to be -1, and "false" to be 0.

    Args:
        command (str): an arithmetic command.
    """
    if command in self.command_functions:
      self.command_functions[command]()

  def write_unary_op(self, command: str, unary_op: str) -> None:
    """Writes the assembly code that is the translation of the given unary operation command."""
    assembly_unary_op = CodeWriter.UNARY_OP.format(command, unary_op)

    self.output_file.write(assembly_unary_op)

  def write_bit_op(self, command: str, bit_op: str) -> None:
    """Writes the assembly code that is the translation of the given bit operation command."""
    assembly_bit_op = CodeWriter.BIT_OP_ASM.format(command, bit_op)

    self.output_file.write(assembly_bit_op)

  def write_cmp(self, command: str) -> None:
    '''Writes the assembly code that is the translation of the gt arithmetic command.'''
    self.comp_op += 1
    asm_command = "J" + command.upper()
    assembly_gt = CodeWriter.COMPARE_ASM.format(command, self.comp_op, asm_command)

    self.output_file.write(assembly_gt)

  def write_push_pop(self, command: str, segment: str, index: int) -> None:
    """Writes assembly code that is the translation of the given 
    command, where command is either C_PUSH or C_POP.

    Args:
        command (str): "C_PUSH" or "C_POP".
        segment (str): the memory segment to operate on.
        index (int): the index in the memory segment.
    """
    
    if command == "C_PUSH":
      if segment == "constant":
        self.constant_push(index)
      elif segment == "temp":
        self.temp_push(index)
      elif segment == "pointer" or segment == "static":
        self.pointer_static_push(segment, index)
      else:
        self.write_push(segment, index)
    elif command == "C_POP":
      if segment == "temp":
        self.temp_pop(index)
      elif segment == "pointer" or segment == "static":
        self.pointer_static_pop(segment, index)
      else:
        self.write_pop(segment, index)

  def pointer_static_push(self, segment: str, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command, where command is
      C_PUSH and segment is static or pointer'''
    
    assembly_pointer_static_push = CodeWriter.PUSH_POINTER_OR_STATIC_ASM.format(segment,
                                                             index,
                                                            self.segment_dic[segment]+int(index))

    self.output_file.write(assembly_pointer_static_push)

    
  def pointer_static_pop(self, segment: str, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_POP and segment is pointer or static'''

    assembly_pointer_static_pop = CodeWriter.POP_STATIC_OR_POINTER.format(segment,
                                                             index,
                                                              self.segment_dic[segment]+int(index))

    self.output_file.write(assembly_pointer_static_pop)

  def temp_push(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_PUSH and segment is temp'''
    assembly_temp_push = CodeWriter.PUSH_TEMP_ASM.format("temp", index, "R5")

    self.output_file.write(assembly_temp_push)

  def temp_pop(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_POP and segment is temp'''
    assembly_temp_pop = CodeWriter.POP_TEMP_ASM.format("temp", index, "R5")

    self.output_file.write(assembly_temp_pop)

  def constant_push(self, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_PUSH and segment is constant'''
    assembly_constant_push = CodeWriter.CONST_PUSH_ASM.format("constant", index, "SP")
    self.output_file.write(assembly_constant_push)

  def write_push(self, segment: str, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_PUSH'''
    assembly_push = CodeWriter.PUSH_ASM.format(segment,
                                                index,
                                                self.segment_dic[segment])

    self.output_file.write(assembly_push)

  def write_pop(self, segment: str, index: int) -> None:
    '''Writes the assembly code that is the translation of the given command,
      where command is C_POP'''
    assembly_pop = CodeWriter.POP_ASM.format(segment, index,
                                              self.segment_dic[segment])

    self.output_file.write(assembly_pop)

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
    if self.current_function == "":
      self.output_file.write(CodeWriter.LABEL_ASM.format(label))
    else:
      self.output_file.write(CodeWriter.FUNC_LABEL_ASM.format(self.current_function, label))

  def write_goto(self, label: str) -> None:
    """Writes assembly code that affects the goto command.

    Args:
        label (str): the label to go to.
    """
    assembly_goto = CodeWriter.GOTO_ASM.format(label)

    self.output_file.write(assembly_goto)

  def write_if(self, label: str) -> None:
    """Writes assembly code that affects the if-goto command. 

    Args:
        label (str): the label to go to.
    """
    assembly_if = CodeWriter.IF_GOTO_ASM.format(label)

    self.output_file.write(assembly_if)

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
    self.current_function = function_name
    self.output_file.write(CodeWriter.FUNCTION_LABEL.format(function_name, self.file_name))
    for i in range(n_vars):
        self.write_push_pop(command="push", segment="constant", index=0)



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
    return_address = CodeWriter.GENERATE_RETURN_LABEL.format(self._cur_method, self.file_name, self.comp_op)
    self.output_file.write(CodeWriter.PUSH_RETURN_LABEL.format(return_address))
    # push LCL              // saves LCL of the caller
    self.output_file.write(CodeWriter.PUSH_ENV_FIELD.format("LCL"))
    # push ARG              // saves ARG of the caller
    self.output_file.write(CodeWriter.PUSH_ENV_FIELD.format("ARG"))
    # push THIS             // saves THIS of the caller
    self.output_file.write(CodeWriter.PUSH_ENV_FIELD.format("THIS"))
    # push THAT             // saves THAT of the caller
    self.output_file.write(CodeWriter.PUSH_ENV_FIELD.format("THAT"))
    # ARG = SP-5-n_args     // repositions ARG
    self.output_file.write(CodeWriter.SET_NEW_ARG.format(f"{n_args}"))
    # LCL = SP              // repositions LCL
    self.output_file.write(CodeWriter.SET_LCL_EQ_SP)
    # goto function_name    // transfers control to the callee
    self.output_file.write(CodeWriter.JUMP_TO_FUNC.format(function_name, self.file_name))
    # (return_address)      // injects the return address label into the code
    self.output_file.write(return_address)
    self.comp_op += 1
    #TODO consider join all the assembly code and then write it to the output file

  def write_return(self) -> None:
    """Writes assembly code that affects the return command."""
    self.output_file.write(CodeWriter.RET_AND_LCL_ADDRESS_ASM.format())
    self.write_pop("argument", 0)
    self.output_file.write(CodeWriter.SP_TO_ARG_PLUS_1_ASM.format())
    self.output_file.write(CodeWriter.END_FRAME_ASM.format("THAT", 1))
    self.output_file.write(CodeWriter.END_FRAME_ASM.format("THIS", 2))
    self.output_file.write(CodeWriter.END_FRAME_ASM.format("ARG", 3))
    self.output_file.write(CodeWriter.END_FRAME_ASM.format("LCL", 4))
    self.write_goto("retAddr")

    
