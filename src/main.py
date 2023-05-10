# Imports
import os

from models.Instructions import InstructionUnit
from models.ReservationStation import ReservationStation
from models.RegisterStatus import RegisterStatus

# Important vars
from important_vars import (
    INSTRUCTION_QUEUE,
    RESERVATION_STATION,
    REGISTER_STATUS,
    COMPLETE_INSTRUCTIONS
)

# Global vars
global CLOCK, QUANTITY_OF_INSTRUCTIONS

def readInstructions(filename: str) -> None:
    with open(filename, 'r') as file:
        for line in file:
            line_args = line.strip().split(" ")
            INSTRUCTION_QUEUE.append(InstructionUnit(line_args[0], line_args[1], line_args[2], line_args[3])) # OP, REGISTER, ARG1, ARG2

def createUnits(loads_fu: int, store_fu: int, add_fu: int, mult_fu: int) -> None:
    for i in range(loads_fu): RESERVATION_STATION[f'Load{i}'] = ReservationStation()
    for i in range(store_fu): RESERVATION_STATION[f'Store{i}'] = ReservationStation()
    for i in range(add_fu): RESERVATION_STATION[f'Add{i}'] = ReservationStation()
    for i in range(mult_fu): RESERVATION_STATION[f'Mult{i}'] = ReservationStation()
    for i in range(0, 31, 2): REGISTER_STATUS[f'F{i}'] = RegisterStatus()

def updateReservationStation(name_type: str, instruction: InstructionUnit) -> str:
    for key in RESERVATION_STATION:
        if RESERVATION_STATION[key].busy == False and key.startswith(name_type):
            RESERVATION_STATION[key].busy = True
            RESERVATION_STATION[key].timeToFinish = instruction.clocks
            RESERVATION_STATION[key].op = instruction.operation
            RESERVATION_STATION[key].D = instruction.register
            return key

def issueInstructions(instruction: InstructionUnit) -> None:
    if instruction.operation in ['ADD', 'SUB']:
        updateReservationStation('Add', instruction)
        #TODO: if else para ver se tem dependencia e atualizar os campos das unidades -> dependencia sera vista na unidade registerStatus
    elif instruction.operation in ['MUL', 'DIV']:
        updateReservationStation('Mult', instruction)
    elif instruction.operation == 'LW':
        updateReservationStation('Load', instruction)
    elif instruction.operation == 'SW':
        updateReservationStation('Store', instruction)

def main() -> None:
    readInstructions("../instructions/instruction1.txt")
    loads_fu = int(input('Digite a quantidade de FU`s de LOAD: '))
    store_fu = int(input('Digite a quantidade de FU`s de STORE: '))
    add_fu = int(input('Digite a quantidade de FU`s de ADD: '))
    mult_fu = int(input('Digite a quantidade de FU`s de MULT: '))
    createUnits(loads_fu, store_fu, add_fu, mult_fu)
    QUANTITY_OF_INSTRUCTIONS = len(INSTRUCTION_QUEUE)
    issueInstructions(INSTRUCTION_QUEUE.pop(0))
    while len(COMPLETE_INSTRUCTIONS) != QUANTITY_OF_INSTRUCTIONS:
        if INSTRUCTION_QUEUE != []:
            issueInstructions(INSTRUCTION_QUEUE.pop(0))

main()