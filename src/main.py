# Imports
import os

from models.Instructions import InstructionUnit
from models.ReservationStation import ReservationStation
from models.RegisterStatus import RegisterStatus
from models.ReorderBuffer import ROB
from models.ReorderBuffer import ROBEntry

# Important vars
from important_vars import (
    INSTRUCTION_QUEUE,
    RESERVATION_STATION,
    REGISTER_STATUS,
    COMPLETE_INSTRUCTIONS
)

# Global vars
global CLOCK

# Instance of units
ROB_UNIT = ROB(10)

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
        reservation_station_name = updateReservationStation('Add', instruction)
        # Verifica se há dependências e atualiza os campos das unidades
        if instruction.arg1.startswith('F') and REGISTER_STATUS[instruction.arg1].Qi is not None:
            if str(REGISTER_STATUS[instruction.arg1].Qi).startswith('VAL'):
                RESERVATION_STATION[reservation_station_name].Vj = REGISTER_STATUS[instruction.arg1].Qi
            else:
                RESERVATION_STATION[reservation_station_name].Qj = REGISTER_STATUS[instruction.arg1].Qi
        else:
                RESERVATION_STATION[reservation_station_name].Vj = instruction.arg1
        if instruction.arg2.startswith('F') and REGISTER_STATUS[instruction.arg2].Qi is not None:
            if str(REGISTER_STATUS[instruction.arg2].Qi).startswith('VAL'):
                RESERVATION_STATION[reservation_station_name].Vk = REGISTER_STATUS[instruction.arg2].Qi
            else:
                RESERVATION_STATION[reservation_station_name].Qk = REGISTER_STATUS[instruction.arg2].Qi
        else:
            RESERVATION_STATION[reservation_station_name].Vk = instruction.arg2
        
        # Atualiza o status do registrador de destino
        if REGISTER_STATUS[instruction.register].Qi is None:
            REGISTER_STATUS[instruction.register].Qi = reservation_station_name
    elif instruction.operation in ['MUL', 'DIV']:
        reservation_station_name = updateReservationStation('Mult', instruction)
        # Verifica se há dependências e atualiza os campos das unidades
        if instruction.arg1.startswith('F') and REGISTER_STATUS[instruction.arg1].Qi is not None:
            if str(REGISTER_STATUS[instruction.arg1].Qi).startswith('VAL'):
                RESERVATION_STATION[reservation_station_name].Vj = REGISTER_STATUS[instruction.arg1].Qi
            else:
                RESERVATION_STATION[reservation_station_name].Qj = REGISTER_STATUS[instruction.arg1].Qi
        else:
                RESERVATION_STATION[reservation_station_name].Vj = instruction.arg1
        if instruction.arg2.startswith('F') and REGISTER_STATUS[instruction.arg2].Qi is not None:
            if str(REGISTER_STATUS[instruction.arg2].Qi).startswith('VAL'):
                RESERVATION_STATION[reservation_station_name].Vk = REGISTER_STATUS[instruction.arg2].Qi
            else:
                RESERVATION_STATION[reservation_station_name].Qk = REGISTER_STATUS[instruction.arg2].Qi
        else:
            RESERVATION_STATION[reservation_station_name].Vk = instruction.arg2
        
        # Atualiza o status do registrador de destino
        if REGISTER_STATUS[instruction.register].Qi is None:
            REGISTER_STATUS[instruction.register].Qi = reservation_station_name
    elif instruction.operation == 'LW':
        # Cria uma nova entrada na estação de reserva Load
        reservation_station_name = updateReservationStation('Load', instruction)
        # Verifica se há dependências e atualiza os campos das unidades
        if instruction.arg1.startswith('F') and REGISTER_STATUS[instruction.arg1].Qi is not None:
            RESERVATION_STATION[reservation_station_name].Qj = REGISTER_STATUS[instruction.arg1].Qi
        else:
            RESERVATION_STATION[reservation_station_name].Vj = instruction.arg1
        # Define o endereço do dado na memória
        RESERVATION_STATION[reservation_station_name].A = instruction.arg2
        
        # Atualiza o status do registrador de destino
        if REGISTER_STATUS[instruction.register].Qi is None:
            REGISTER_STATUS[instruction.register].Qi = reservation_station_name
    elif instruction.operation == 'SW':
         # Cria uma nova entrada na estação de reserva Store
        reservation_station_name = updateReservationStation('Store', instruction)
        # Verifica se há dependências e atualiza os campos das unidades
        if instruction.arg1.startswith('F') and REGISTER_STATUS[instruction.arg1].Qi is not None:
            RESERVATION_STATION[reservation_station_name].Qj = REGISTER_STATUS[instruction.arg1].Qi
        else:
            RESERVATION_STATION[reservation_station_name].Vj = instruction.arg1
        if instruction.arg2.startswith('F') and REGISTER_STATUS[instruction.arg2].Qi is not None:
            RESERVATION_STATION[reservation_station_name].Qk = REGISTER_STATUS[instruction.arg2].Qi
        else:
            RESERVATION_STATION[reservation_station_name].Vk = instruction.arg2
        # Define o endereço do dado na memória
        RESERVATION_STATION[reservation_station_name].A = instruction.register
        
        # Atualiza o status do registrador de destino
        if REGISTER_STATUS[instruction.register].Qi is None:
            REGISTER_STATUS[instruction.register].Qi = reservation_station_name
    else:
        print(str(instruction.operation) + " não é válido.")


def updateUnits() -> None:
    for chave in RESERVATION_STATION:
        if RESERVATION_STATION[chave].busy == True:
            if RESERVATION_STATION[chave].timeToFinish == 0:
                # TODO: Termina a execução e tira da reservation station - atualiza register status VAL(Chave) - update no Vj e Vk com base no QJ e Qk
                REGISTER_STATUS[RESERVATION_STATION[chave].D].Qi = f'VAL({chave})'
                for sub_chave in RESERVATION_STATION:
                    if RESERVATION_STATION[sub_chave].Qj == chave:
                        RESERVATION_STATION[sub_chave].Qj = None
                        RESERVATION_STATION[sub_chave].Vj = f'VAL({chave})'
                    elif RESERVATION_STATION[sub_chave].Qk == chave:
                        RESERVATION_STATION[sub_chave].Qk = None
                        RESERVATION_STATION[sub_chave].Vk = f'VAL({chave})'
                RESERVATION_STATION[chave] = ReservationStation()
            else:
                if RESERVATION_STATION[chave].Qj == None and RESERVATION_STATION[chave].Qk == None:
                    RESERVATION_STATION[chave].timeToFinish -= 1

def isReservationEmpty() -> bool:
    for chave in RESERVATION_STATION: 
        if RESERVATION_STATION[chave].busy == True:
            return False
    return True

def printInformation():
    print(f'-------------- CLOCK {CLOCK} --------------')
    print(f'-------------- INSTRUCTION QUEUE STATION --------------')
    for i in INSTRUCTION_QUEUE:
        print(str(i))
    print("\n")

    print(f'-------------- RESERVATION STATION --------------')
    for i in RESERVATION_STATION:
            print(str(i) + " " + str(RESERVATION_STATION[i]))
    print("\n")

    print(f'-------------- REGISTER STATUS --------------')
    for i in REGISTER_STATUS:
        print(str(i) + " " + str(REGISTER_STATUS[i]))
    print("\n")

    print(ROB_UNIT)
    print("\n")


def runProgram() -> None:
    global CLOCK

    CLOCK = 0
    printInformation()
    issueInstructions(INSTRUCTION_QUEUE.pop(0))
    CLOCK += 1
    while not isReservationEmpty():
        printInformation()
        CLOCK += 1
        updateUnits()
        if INSTRUCTION_QUEUE != []:
            issueInstructions(INSTRUCTION_QUEUE.pop(0))
    printInformation()

    
def main() -> None:
    readInstructions("../instructions/instruction1.txt")
    loads_fu = 3
    store_fu = 3
    add_fu = 3
    mult_fu = 3
    createUnits(loads_fu, store_fu, add_fu, mult_fu)
    runProgram()

main()