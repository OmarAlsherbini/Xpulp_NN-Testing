# Python Codes to Read Xpulp_NN ISA & Generate Test Programs
The code is divided into two sections; a section for each sheet of the ISA Excel file. The Excel file is also converted into CSV to be able to be processed via Pandas. Both Python and Jupyter versions are provided.
## 1) Foglio1 ISA:
For the first sheet, the code combines the hexes of the OP MASK (Col O) and the VV/VS MASK (Col Q) into the instruction mask, adding 0x00940700 to the resulting hex in order to assert that rs1 is x8, rs2 is x9 and rd is x14.  
The code then proceeds to output the hex of the following assembly test program for each instruction in the CSV in a seperate file with the name of the instruction mnemonic:  
```assembly  
.globl __start  
  
__start:  
  li x8, 10  
  li x9, 12  
  li x15, 0x75D321F6  
  bltz x15, 16  
  li x14, 19  
  blt x8, x9, 8  
  li x13, 15  
  
  # Xpulp_NN INSTR here. Example:  
  pv.sdotusp.sc.n x14, x8, x9  
    
  li x16, 0x00010048  
  sw x16, x14, 4  
  # Terminate RI5CY TB  
  li x18, 0x20000000  
  li x19, 123456789  
  sw x18, x19, 0  
  # ends the program with status code 0  
  li a0, 10  
  ecall  
  ```
The code also outputs the makefile instructions necessary to run each hex file on the CV32E40P core in a file called "make_add.txt".  
Finally, the code outputs all the Xpulp_NN hex instuctions - without the test program mentioned above - in single files, formatted into 0xHEX format, HEX format, big endian format, 4 big endian instructions format and continuous big endian format.   
## 2) newest_version ISA:
The same happens for this sheet. The code outputs the same test program mentioned above for each hex for each instruction. However, this time the hexes are already prepared for each instruction in the file itself in advance, letting rd be x14, rs1 be x8 and immediate be 9 as the following example:  
pv.mlsdotsup.h x14, x8, 0x9  
The code also adds the make file instructions necessary to run the test programs (TPs) in make_add2.txt.  
## How to Use
1) Put the test programs to be run (either from TPs (first sheet TPs) or from newest_TPs (second sheet TPs)) in example_tb/core/xpulp_tests (create this folder if it doesn't exist).  
2) Append the makefile .PHONY instructions by copying them from make_add.txt and make_add2.txt.  
3) Run the makefile for the desired instruction.  
