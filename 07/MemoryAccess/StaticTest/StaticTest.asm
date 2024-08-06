// push const 111
@111
D=A
@SP
M=M+1
A=M-1
M=D
// push const 333
@333
D=A
@SP
M=M+1
A=M-1
M=D
// push const 888
@888
D=A
@SP
M=M+1
A=M-1
M=D
// pop static
@SP
M=M-1
A=M
D=M
@StaticTest.8
M=D
// pop static
@SP
M=M-1
A=M
D=M
@StaticTest.3
M=D
// pop static
@SP
M=M-1
A=M
D=M
@StaticTest.1
M=D
// push static 3
@StaticTest.3
D=M
@SP
M=M+1
A=M-1
M=D
// push static 1
@StaticTest.1
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
// push static 8
@StaticTest.8
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
