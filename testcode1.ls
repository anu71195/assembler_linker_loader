JMP #4
DB 0
JMP #8
DB 1
JMP #12
DB 1
PUSH D
MVI E,5
LDA #3
MOV B,A
LDA #7
ADD B
STA #3
LDA #7
ADI 1
STA #7
MOV A,E
SUI 1
MOV E,A
JNZ #15
POP D