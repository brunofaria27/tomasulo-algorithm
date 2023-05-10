# Imports
import os

from models.Instructions import InstructionUnit
from models.ReservationStation import ReservationStation
from models.RegisterStatus import RegisterStatus

# Important vars
from important_vars import (
    INSTRUCTION_QUEUE,
    RESERVATION_STATION,
    REGISTER_STATUS
)

# Global vars
global CLOCK

def readInstructions(filename: str) -> None:
    with open(filename, 'r') as file:
        for line in file:
            line_args = line.strip().split(" ")
            INSTRUCTION_QUEUE.append(InstructionUnit(line_args[0], line_args[1], line_args[2], line_args[3])) # OP, REGISTER, ARG1, ARG2

def createUnits(loads_fu: int, store_fu: int, add_fu: int, mult_fu: int) -> None:
    for i in range(loads_fu): RESERVATION_STATION.append(ReservationStation(f'Load{i}'))
    for i in range(store_fu): RESERVATION_STATION.append(ReservationStation(f'Store{i}'))
    for i in range(add_fu): RESERVATION_STATION.append(ReservationStation(f'Add{i}'))
    for i in range(mult_fu): RESERVATION_STATION.append(ReservationStation(f'Mult{i}'))
    for i in range(0, 31, 2): REGISTER_STATUS.append(RegisterStatus(f'F{i}'))

def main() -> None:
    readInstructions("../instructions/instruction1.txt")
    loads_fu = int(input('Digite a quantidade de FU`s de LOAD: '))
    store_fu = int(input('Digite a quantidade de FU`s de STORE: '))
    add_fu = int(input('Digite a quantidade de FU`s de ADD: '))
    mult_fu = int(input('Digite a quantidade de FU`s de MULT: '))
    createUnits(loads_fu, store_fu, add_fu, mult_fu)
    os.system('cls') # Clear console -> Change to clear if you use a Unix OS
    print('--------------- INSTRUCTION QUEUE ---------------')
    for i in INSTRUCTION_QUEUE:
        print(i)
    print(f'--------------- RESERVATION STATION ---------------')
    for i in RESERVATION_STATION:
        print(i)
    print('--------------- REGISTER STATUS ---------------')
    for i in REGISTER_STATUS:
        print(i)

        

main()