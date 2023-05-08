# Imports
from models.instructions import InstructionUnit

# Consts
from important_vars import INSTRUCTIONS, INSTRUCTION_QUEUE

def readInstructions(filename: str) -> None:
    with open(filename, 'r') as file:
        for line in file:
            line_args = line.strip().split(" ")
            INSTRUCTIONS.append([line_args[0], line_args[1], line_args[2], line_args[3]]) # OP, REGISTER, ARG1, ARG2

def createInstructions() -> None:
    for instruction in INSTRUCTIONS:
        INSTRUCTION_QUEUE.append(InstructionUnit(instruction[0], instruction[1], instruction[2], instruction[3]))

def main() -> None:
    readInstructions("../instructions\instruction1.txt")
    createInstructions()
    for i in INSTRUCTION_QUEUE:
        print(i.printInstruction())

main()