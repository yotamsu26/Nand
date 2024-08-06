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


@1
D=A
@R0
M=D
@32767
(LABEL)
D=A+1
@R0
M=M+1
@LABEL
D;JLT
@3
D=A
@R0
D-M;JNE