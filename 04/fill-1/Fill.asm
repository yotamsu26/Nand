// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// pseudo code :
// while true :
//   if (keyboard is pressed): 
//     x = -1
//   else :
//     x = 0
//   for i in screen memo :
//     screenmemo[i] = x


(START)

@SCREEN
D=A
@address
M=D	// save the screen left up corner location in memory

@8192
D=A // insert the value 8192 to D its the number of full screen pixles 
	// calculation : 512*256/16
@n
M=D // n = number to store, the number of pixles left to change


(PRESSCHECK)

@KBD
D=M
@BLACK
D;JGT	// if any keyboard is pressed the KBD store a number bigger than when
		// and the screen need to be black colored, so jump to the relevant 		// code
@WHITE
D;JEQ	// if no keyboard is pressed the KBD store zero
		// and the screen need to be white colored, so jump to the relevant 		// code
				
@PRESSCHECK // always jump after finishing to change the screen to the 
0;JMP		// relevant color.


(BLACK) // the code to store the black color in memory
@COLOR
M=-1	// (-1=11111111111111) what to fill in the screen
@LOOP
0;JMP


(WHITE) // the code to store the white color in memory
@COLOR
M=0	// what to fill in the screen
@LOOP
0;JMP


(LOOP) // iterate over the intire screen
@COLOR	//check what to fill the screen with
D=M	

@address
A=M	// the pixel to fill
M=D	

@n
M=M-1	
D=M

@address
M=M+1	// move the the next pixel location
A=M

@LOOP
D;JGT	//IF A=0 EXIT AS THE WHOLE SCREEN IS BLACK


@START
0;JMP