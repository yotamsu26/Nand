// push constant 3030
@3030
D=A
@SP
M=M+1
A=M-1
M=D
// pop pointer 0
@SP
M=M-1
A=M
D=M
@3
M=D
// push constant 3040
@3040
D=A
@SP
M=M+1
A=M-1
M=D
// pop pointer 1
@SP
M=M-1
A=M
D=M
@4
M=D
// push constant 32
@32
D=A
@SP
M=M+1
A=M-1
M=D
// pop this 2
@2
D=A
@THIS
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push constant 46
@46
D=A
@SP
M=M+1
A=M-1
M=D
// pop that 6
@6
D=A
@THAT
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push pointer 0
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push pointer 1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
// add operation
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
// push this 2
@2
D=A
@THIS
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
// sub operation
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
// push that 6
@6
D=A
@THAT
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
// add operation
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
