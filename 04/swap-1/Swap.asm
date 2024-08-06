// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

// pseudo code :
// for i in arr.len :
//    if arr[i] > max:
//		 max = arr[i]
//    elif arr[i] < min:
//       mix = arr[i]
// swap max and min

    //max = min = the first array value
    @R14
	D=M
    @max
    M=D
    @min
    M=D
    @current
    M=D
	@R15
	D=M
	@END
	D;JEQ
	@i
	M=D
	M=M-1

(LOOP)
	// jump to swap in the and of the loop
	@i
	D=M
	@SWAP
	D;JEQ
	
	// check if bigger than max
	@current
	M=M+1  // inc current every iteration
	A=M
	D=M
	@max
	A=M
	D=D-M
	@REPLACEMAX
	D;JGT
	
	// check if smaller than min
	@current
	A=M
	D=M
	@min
	A=M
	D=M-D
	@REPLACEMIN
	D;JGT 
	
	// go to the next iteration
	@i
	M=M-1
	@LOOP
	0;JMP
	
(REPLACEMAX)
	// gets here if current > max
	@current
	D=M
	@max
	M=D
	@i
	M=M-1
	@LOOP
	0;JMP

(REPLACEMIN)
	// gets here if current < min
	@current
	D=M
	@min
	M=D
	@i
	M=M-1
	@LOOP
	0;JMP
	
(SWAP)
	// swap max and min
	@min
	A=M
	D=M
	@temp
	M=D
	@max
	A=M
	D=M
	@min
	A=M
	M=D
	@temp
	D=M
	@max
	A=M
	M=D
	
(END)
    @END
    0;JMP
	


    