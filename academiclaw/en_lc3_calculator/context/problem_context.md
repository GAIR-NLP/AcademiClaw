# Problem Context: LC-3 Stack Calculator

## LC-3 Conventions

- **Stack**: Grows from high address to low address; common stack region BASE is x3FFF, MAX is x3FFB; **R6** is the stack pointer (points to the top element).
- **PUSH**: Decrement R6 by 1 then write R0; if R6 has reached MAX, the stack is full and R5=1 indicates failure; otherwise R5=0.
- **POP**: Read from R6 into R0, then increment R6 by 1; if the stack is empty, R5=1; otherwise R5=0.
- **Operations**: Results must be within **[-999, 999]**; otherwise report an error and restore the stack (do not modify stack contents).

## Instructions and Commands

- Command **X**: Exit (HALT).
- **C**: Clear the stack (reinitialize R6).
- **+**, **\***, **%**, **@** (XOR), **neg**: Binary or unary operations; POP operands, compute, RangeCheck, PUSH result.
- **D**: Display the stack top (without popping).
- Digits: Push an integer onto the stack (must handle multi-digit input).

## Context File Descriptions

- `10.push.asm`, `10.pop.asm`, etc. are reference snippets (corresponding to textbook figures), containing PUSH/POP and some Op implementation ideas.
- The various .asm snippets can be referenced for interfaces and flow; your solution must be completed independently.
- All .asm files are LC-3 assembly, using `.ORIG`, `.FILL`, `.STRINGZ`, `.BLKW` and other pseudo-instructions.

## Constraints

- Do not rely on special extensions of external assemblers or simulators; use only standard LC-3 instructions and pseudo-instructions.
- Stack operation and computation interface conventions (R5 success/failure, R6 stack pointer) must match the task requirements.
