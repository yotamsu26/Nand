// push const 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
// push const 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
// eq operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE0
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE0
D;JLT
@R13
D=D-M
@INSERT0
0;JMP
(Y_NEGATIVE0)
@SP
A=M-1
D=M
@Y_X_NEGATIVE0
D;JLT
D=1
@INSERT0
0;JMP
(X_NEGATIVE0)
D = -1
@INSERT0
0;JMP
(Y_X_NEGATIVE0)
@R13
D=D-M
@INSERT0
0;JMP
(INSERT0)
@INESRT_TRUE0
D;JEQ
@SP
A=M-1
M=0
@CONTINUE0
0;JMP
(INESRT_TRUE0)
@SP
A=M-1
M=-1
(CONTINUE0)
// push const 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
// push const 16
@16
D=A
@SP
M=M+1
A=M-1
M=D
// eq operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE1
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE1
D;JLT
@R13
D=D-M
@INSERT1
0;JMP
(Y_NEGATIVE1)
@SP
A=M-1
D=M
@Y_X_NEGATIVE1
D;JLT
D=1
@INSERT1
0;JMP
(X_NEGATIVE1)
D = -1
@INSERT1
0;JMP
(Y_X_NEGATIVE1)
@R13
D=D-M
@INSERT1
0;JMP
(INSERT1)
@INESRT_TRUE1
D;JEQ
@SP
A=M-1
M=0
@CONTINUE1
0;JMP
(INESRT_TRUE1)
@SP
A=M-1
M=-1
(CONTINUE1)
// push const 16
@16
D=A
@SP
M=M+1
A=M-1
M=D
// push const 17
@17
D=A
@SP
M=M+1
A=M-1
M=D
// eq operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE2
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE2
D;JLT
@R13
D=D-M
@INSERT2
0;JMP
(Y_NEGATIVE2)
@SP
A=M-1
D=M
@Y_X_NEGATIVE2
D;JLT
D=1
@INSERT2
0;JMP
(X_NEGATIVE2)
D = -1
@INSERT2
0;JMP
(Y_X_NEGATIVE2)
@R13
D=D-M
@INSERT2
0;JMP
(INSERT2)
@INESRT_TRUE2
D;JEQ
@SP
A=M-1
M=0
@CONTINUE2
0;JMP
(INESRT_TRUE2)
@SP
A=M-1
M=-1
(CONTINUE2)
// push const 892
@892
D=A
@SP
M=M+1
A=M-1
M=D
// push const 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
// lt operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE3
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE3
D;JLT
@R13
D=D-M
@INSERT3
0;JMP
(Y_NEGATIVE3)
@SP
A=M-1
D=M
@Y_X_NEGATIVE3
D;JLT
D=1
@INSERT3
0;JMP
(X_NEGATIVE3)
D = -1
@INSERT3
0;JMP
(Y_X_NEGATIVE3)
@R13
D=D-M
@INSERT3
0;JMP
(INSERT3)
@INESRT_TRUE3
D;JLT
@SP
A=M-1
M=0
@CONTINUE3
0;JMP
(INESRT_TRUE3)
@SP
A=M-1
M=-1
(CONTINUE3)
// push const 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
// push const 892
@892
D=A
@SP
M=M+1
A=M-1
M=D
// lt operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE4
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE4
D;JLT
@R13
D=D-M
@INSERT4
0;JMP
(Y_NEGATIVE4)
@SP
A=M-1
D=M
@Y_X_NEGATIVE4
D;JLT
D=1
@INSERT4
0;JMP
(X_NEGATIVE4)
D = -1
@INSERT4
0;JMP
(Y_X_NEGATIVE4)
@R13
D=D-M
@INSERT4
0;JMP
(INSERT4)
@INESRT_TRUE4
D;JLT
@SP
A=M-1
M=0
@CONTINUE4
0;JMP
(INESRT_TRUE4)
@SP
A=M-1
M=-1
(CONTINUE4)
// push const 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
// push const 891
@891
D=A
@SP
M=M+1
A=M-1
M=D
// lt operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE5
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE5
D;JLT
@R13
D=D-M
@INSERT5
0;JMP
(Y_NEGATIVE5)
@SP
A=M-1
D=M
@Y_X_NEGATIVE5
D;JLT
D=1
@INSERT5
0;JMP
(X_NEGATIVE5)
D = -1
@INSERT5
0;JMP
(Y_X_NEGATIVE5)
@R13
D=D-M
@INSERT5
0;JMP
(INSERT5)
@INESRT_TRUE5
D;JLT
@SP
A=M-1
M=0
@CONTINUE5
0;JMP
(INESRT_TRUE5)
@SP
A=M-1
M=-1
(CONTINUE5)
// push const 32767
@32767
D=A
@SP
M=M+1
A=M-1
M=D
// push const 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
// gt operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE6
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE6
D;JLT
@R13
D=D-M
@INSERT6
0;JMP
(Y_NEGATIVE6)
@SP
A=M-1
D=M
@Y_X_NEGATIVE6
D;JLT
D=1
@INSERT6
0;JMP
(X_NEGATIVE6)
D = -1
@INSERT6
0;JMP
(Y_X_NEGATIVE6)
@R13
D=D-M
@INSERT6
0;JMP
(INSERT6)
@INESRT_TRUE6
D;JGT
@SP
A=M-1
M=0
@CONTINUE6
0;JMP
(INESRT_TRUE6)
@SP
A=M-1
M=-1
(CONTINUE6)
// push const 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
// push const 32767
@32767
D=A
@SP
M=M+1
A=M-1
M=D
// gt operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE7
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE7
D;JLT
@R13
D=D-M
@INSERT7
0;JMP
(Y_NEGATIVE7)
@SP
A=M-1
D=M
@Y_X_NEGATIVE7
D;JLT
D=1
@INSERT7
0;JMP
(X_NEGATIVE7)
D = -1
@INSERT7
0;JMP
(Y_X_NEGATIVE7)
@R13
D=D-M
@INSERT7
0;JMP
(INSERT7)
@INESRT_TRUE7
D;JGT
@SP
A=M-1
M=0
@CONTINUE7
0;JMP
(INESRT_TRUE7)
@SP
A=M-1
M=-1
(CONTINUE7)
// push const 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
// push const 32766
@32766
D=A
@SP
M=M+1
A=M-1
M=D
// gt operation
@SP
M=M-1
A=M
D=M
@R13
M=D
@Y_NEGATIVE8
D;JLT
@SP
A=M-1
D=M
@X_NEGATIVE8
D;JLT
@R13
D=D-M
@INSERT8
0;JMP
(Y_NEGATIVE8)
@SP
A=M-1
D=M
@Y_X_NEGATIVE8
D;JLT
D=1
@INSERT8
0;JMP
(X_NEGATIVE8)
D = -1
@INSERT8
0;JMP
(Y_X_NEGATIVE8)
@R13
D=D-M
@INSERT8
0;JMP
(INSERT8)
@INESRT_TRUE8
D;JGT
@SP
A=M-1
M=0
@CONTINUE8
0;JMP
(INESRT_TRUE8)
@SP
A=M-1
M=-1
(CONTINUE8)
// push const 57
@57
D=A
@SP
M=M+1
A=M-1
M=D
// push const 31
@31
D=A
@SP
M=M+1
A=M-1
M=D
// push const 53
@53
D=A
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
// push const 112
@112
D=A
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
// neg operation
@SP
A=M-1
M=-M
// and operation
@SP
M=M-1
A=M
D=M
A=A-1
M=M&D
// push const 82
@82
D=A
@SP
M=M+1
A=M-1
M=D
// or operation
@SP
M=M-1
A=M
D=M
A=A-1
M=M|D
// not operation
@SP
A=M-1
M=!M
