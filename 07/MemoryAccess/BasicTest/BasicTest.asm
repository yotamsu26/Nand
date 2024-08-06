// push const 10
@10
D=A
@SP
M=M+1
A=M-1
M=D
// pop local 0
@0
D=A
@LCL
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
// push const 21
@21
D=A
@SP
M=M+1
A=M-1
M=D
// push const 22
@22
D=A
@SP
M=M+1
A=M-1
M=D
// pop argument 2
@2
D=A
@ARG
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
// pop argument 1
@1
D=A
@ARG
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
// push const 36
@36
D=A
@SP
M=M+1
A=M-1
M=D
// pop this 6
@6
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
// push const 42
@42
D=A
@SP
M=M+1
A=M-1
M=D
// push const 45
@45
D=A
@SP
M=M+1
A=M-1
M=D
// pop that 5
@5
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
// pop that 2
@2
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
// push const 510
@510
D=A
@SP
M=M+1
A=M-1
M=D
// pop temp 6
@6
D=A
@5
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push local 0
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
// push that 5
@5
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
// push argument 1
@1
D=A
@ARG
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
// push this 6
@6
D=A
@THIS
D=D+M
A=D
D=M
@SP
M=M+1
A=M-1
M=D
// push this 6
@6
D=A
@THIS
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
// sub operation
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
// push temp 6
@6
D=A
@5
A=A+D
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
