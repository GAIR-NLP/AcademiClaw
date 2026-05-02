# Operation List: LC-3 Stack Calculator Implementation Steps

## 1. Read the Problem and Context

- Read `workspace/query.md` for command descriptions and deliverable requirements.
- Read `context/problem_context.md` for stack conventions, R5/R6 interface, and range requirements.
- Browse the .asm reference snippets under context (e.g., 10.push.asm, 10.pop.asm, 10.10.asm through 10.27.asm), corresponding to the main loop, OpAdd, OpMult, POP, PUSH, and other logic.

## 2. Implement Stack Subroutines

- **PUSH**: Check if the stack is full (compare R6 with MAX). If full, set R5=1 and return; otherwise decrement R6 by 1, store R0 into (R6), set R5=0, and return.
- **POP**: Check if the stack is empty (compare R6 with BASE). If empty, set R5=1 and return; otherwise load from (R6) into R0, increment R6 by 1, set R5=0, and return.
- Refer to implementations in `10.push.asm`, `10.pop.asm`, or `10.23.asm`, etc.

## 3. Implement Main Loop and Command Dispatch

- Initialization: Set R6 to the stack base (e.g., StackBase), display a prompt "Enter a command:", and use GETC to read a character.
- Branch based on the character: X -> Exit, C -> OpClear, + -> OpAdd, * -> OpMult, % -> Opmod, @ -> OpXOR, neg -> Opneg, D -> OpDisplay, digit -> PushValue.
- Refer to the main program structure in context (e.g., the Test/NewCommand portion of reference_lab2.asm).

## 4. Implement Operations and Helper Routines

- **OpAdd / OpMult / Opmod / OpXOR**: Two POPs, perform the operation, RangeCheck; if successful, PUSH the result and continue; if failed, restore the stack (adjust R6) and return.
- **Opneg**: One POP, negate, RangeCheck, PUSH.
- **RangeCheck**: If the result is outside [-999, 999], print an error and return R5=1.
- **OpClear**: Point R6 to the stack base. **OpDisplay**: Display the stack top (without POP).
- Refer to snippets 10.10, 10.14, 10.15, 10.26, etc. in context.

## 5. Output and Deliverables

- Save the complete program as **lab2.asm** (or answer.asm / solution.asm) in the current directory.
- The program should include .ORIG x3000, all subroutines, and the data section (stack, prompt strings, constants, etc.).
- Evaluation is performed by eval_task calling eval/rubric.py; context only contains background material and reference code, not the evaluation script.
