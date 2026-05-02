# Query: LC-3 Stack-Based Calculator

## Task Description

Implement a stack-based calculator program using **LC-3 assembly**. The program reads commands and operands from user input and supports the following features:

- **X**: Exit.
- **C**: Clear the stack.
- **+**, **\***, **%**, **@** (XOR), **neg** (negate): Pop operand(s) from the stack top, perform the operation, and push the result; the result must be within [-999, 999], otherwise report an error and restore the stack.
- **D**: Display the stack top (without popping).
- **Digits**: Push a valid integer onto the stack.

The stack grows from high address to low address. The stack region can be a fixed range (e.g., x3FFF to x3FFB). **R6** is the stack pointer. You must implement **PUSH** and **POP** subroutines, with the convention that **R5=0** indicates success and **R5=1** indicates failure (stack empty/full, etc.).

## Workflow

1. **Read context**
   - Read `context/problem_context.md` for LC-3 conventions, stack, and instruction set details.
   - Read `context/operation_list.md` for recommended implementation steps and correspondence with reference code in context.

2. **Implement PUSH / POP**
   - Refer to the stack implementations in context (e.g., 10.push.asm, 10.pop.asm), implement PUSH and POP that follow the task conventions, and correctly maintain R6 and R5.

3. **Implement operations and main loop**
   - Implement OpAdd, OpMult, Opmod, OpXOR, Opneg, OpClear, OpDisplay, etc. The main loop dispatches to the corresponding handler based on the input character, or pushes a number.
   - Pay attention to range checking (e.g., -999 to 999) and restoring the stack on error.

4. **Output**
   - Save the complete LC-3 assembly program to **lab2.asm** (or **answer.asm** / **solution.asm**) in the current directory. The program should begin with `.ORIG x3000` and include all subroutines and the data section.

## Constraints and Assumptions (from Context)

- Use the LC-3 instruction set; stack region and register conventions are specified in context.
- Do not depend on external tools or files other than those in context.
- The .asm files in context are reference snippets (corresponding to textbook figures); you may reference their logic and interfaces, but must independently produce a complete, assembleable, runnable program.

## Deliverables

- **lab2.asm** (or answer.asm / solution.asm): Complete LC-3 assembly source program, including main program, PUSH/POP, all operation subroutines, and data definitions.

## Notes

- Ensure POP returns failure when the stack is empty and PUSH returns failure when the stack is full; when operation results are out of range, report an error and restore the stack as required.
- Evaluation is performed by eval_task calling eval/rubric.py; context only contains background material and reference code, not the evaluation script.
