# Imports
from models.Instructions import InstructionUnit

# Important vars
from important_vars import INSTRUCTION_QUEUE

# Global vars
global CLOCK

def readInstructions(filename: str) -> None:
    with open(filename, 'r') as file:
        for line in file:
            line_args = line.strip().split(" ")
            INSTRUCTION_QUEUE.append(InstructionUnit(line_args[0], line_args[1], line_args[2], line_args[3])) # OP, REGISTER, ARG1, ARG2

def main() -> None:
    readInstructions("../instructions/instruction1.txt")
    for instruction in INSTRUCTION_QUEUE:
        print(instruction)
        

main()