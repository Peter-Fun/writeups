# Binary Blast Writeup
## Description
nc 0.cloud.chals.io 12490

Ready for a blast from the past? Navigate the MIPS landscape and watch out for those sneaky format strings. Beware of fake flags—only the real one will do!

Author: LMS
## Solution
### Part 1: Exploring
Based off of the description, we can see that MIPS will play a role in this challenge, which is an instruction set architecture like x86 and arm. 

Likewise, we can see it when running the "file" command on the binary, also seeing that it is a PIE executable.

![file](source/1.png)

PIE, or Position Independent Executable, is used to allow random memory allocation of the executable that is usually used with ASLR, or Address Space Layout Randomization, in order to randomly set address space locations for the data in the executable and making it not possible to hardcode used addresses. 

There is a workaround though, being that the addresses are still the same relative to each other, meaning that if we could get a known address and its position relative to other addresses, we can use the fact that the offsets always remains constant between memory address between runs to still be able to get memory addresses of other parts of the binary.

To actually start running and debugging the binary file, qemu-mips was provided along with the challenge, and we were 

### Part 2: Analyzing


### Part 3: Exploiting
