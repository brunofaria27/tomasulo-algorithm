CLOCK_TIME_INSTRUCTION = {"LW": 2, "SW": 2, "ADD": 2, "SUB": 2, "MUL": 5, "DIV": 40}
INSTRUCTION_QUEUE = []
RESERVATION_STATION = {}
REGISTER_STATUS = {}
REORDER_BUFFER = {}
COMPLETE_INSTRUCTIONS = []

class InstructionUnit:
    def __init__(self, operation: str, register: str, arg1: str, arg2: str) -> None:
        self.operation = operation
        self.register = register
        self.arg1 = arg1
        self.arg2 = arg2
        self.isIssued = False
        self.isStarted = False
        self.isWritten = False
        self.isFinished = False
        self.clocks = CLOCK_TIME_INSTRUCTION[operation]
        self.clocksLeft = CLOCK_TIME_INSTRUCTION[operation]
        self.isIssuedClock = -1
        self.isStartedClock = -1
        self.isWrittenClock = -1
        self.isFinishedClock = -1

    def __str__(self) -> str:
        return "[Operation: " + str(self.operation) + ", Register: " + str(self.register) + ", Argument 1: " + str(self.arg1) + ", Argument 2: " + str(
            self.arg2) + ", Issued: " + str(self.isIssued) + ", Started: " + str(self.isStarted) + ", Written: " + str(
            self.isWritten) + ", Finished: " + str(self.isFinished) + ", Clocks: " + str(self.clocks) + ", Clocks left: " + str(
            self.clocksLeft) + ", Issued Clock: " + str(self.isIssuedClock) + ", Started Clock: " + str(self.isStartedClock) + ", Written Clock: " + str(
            self.isWrittenClock) + ", FinishedClock: " + str(self.isFinishedClock) + "]"
    
class RegisterStatus:
    def __init__(self) -> None:
        self.Qi = None
    
    def __str__(self) -> str:
        return "[Qi: " + str(self.Qi) + "]"
    
class ReservationStation:
    def __init__(self) -> None:
        self.timeToFinish = -1
        self.busy = False
        self.op = None
        self.D = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None # Only used in LW and SW
        self.ROBId = None

    def __str__(self) -> str:
        return "[Time to finish: " + str(self.timeToFinish) + ", Busy: " + str(self.busy) + ", Op: " + str(self.op) + ", Destination: " + str(self.D) + ", Vj: " + str(self.Vj) + ", Vk: " + str(
            self.Vk) + ", Qj: " + str(self.Qj) + ", Qk: " + str(self.Qk) + ", A: " + str(self.A) + ", ROB Id: " + str(self.ROBId) + "]"
    
class ROBEntry:
    def __init__(self):
        self.instruction = None
        self.destination = None
        self.value = None
        self.ready = False
        self.reservationStation = None
        self.leftReservationStation = False

    def executeOperations(self, instruction_reservation: ReservationStation) -> str:
        if instruction_reservation.op == 'LW':
            return f'VAL({str(instruction_reservation.Vj) + " + " + str(instruction_reservation.A)})'
        elif instruction_reservation.op == 'SW':
            return f'VAL({str(instruction_reservation.Vj) + " + " + str(instruction_reservation.A)})'
        elif instruction_reservation.op == 'SUB':
            return f'VAL({str(instruction_reservation.Vj) + " - " + str(instruction_reservation.Vk)})'
        elif instruction_reservation.op == 'ADD':
            return f'VAL({str(instruction_reservation.Vj) + " + " + str(instruction_reservation.Vk)})'
        elif instruction_reservation.op == 'MUL':
            return f'VAL({str(instruction_reservation.Vj) + " * " + str(instruction_reservation.Vk)})'
        elif instruction_reservation.op == 'DIV':
            return f'VAL({str(instruction_reservation.Vj) + " / " + str(instruction_reservation.Vk)})'

    def __str__(self):
        return f"[Instruction: {self.instruction}, Destination: {self.destination}, Ready: {self.ready}, Value: {self.value}, Reservation Station name: {self.reservationStation}, Left reservation station: {self.leftReservationStation}]"

# Global vars
global CLOCK

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
    for i in range(10): REORDER_BUFFER[f'ROB{i}'] = ROBEntry()
    for i in range(0, 31, 2): REGISTER_STATUS[f'F{i}'] = RegisterStatus()


def updateReservationStation(name_type: str, instruction: InstructionUnit) -> str:
    for key in RESERVATION_STATION:
        if RESERVATION_STATION[key].busy == False and key.startswith(name_type):
            RESERVATION_STATION[key].busy = True
            RESERVATION_STATION[key].timeToFinish = instruction.clocks
            RESERVATION_STATION[key].op = instruction.operation
            RESERVATION_STATION[key].D = instruction.register
            return key
        

def addROBInstruction(instruction: str, destination: str, reservation_station_name: str) -> str:
    for key in REORDER_BUFFER:
        if REORDER_BUFFER[key].instruction is None:
            REORDER_BUFFER[key].instruction = instruction
            REORDER_BUFFER[key].destination = destination
            REORDER_BUFFER[key].reservationStation = reservation_station_name
            return key


def issueInstructions(instruction: InstructionUnit) -> None:

    if instruction.operation in ['ADD', 'SUB']:
        reservation_station_name = updateReservationStation('Add', instruction)
        rob_name = addROBInstruction(instruction.operation, instruction.register, reservation_station_name)
        RESERVATION_STATION[reservation_station_name].ROBId = rob_name
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
        rob_name = addROBInstruction(instruction.operation, instruction.register, reservation_station_name)
        RESERVATION_STATION[reservation_station_name].ROBId = rob_name
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
        rob_name = addROBInstruction(instruction.operation, instruction.register, reservation_station_name)
        RESERVATION_STATION[reservation_station_name].ROBId = rob_name
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
        rob_name = addROBInstruction(instruction.operation, instruction.register, reservation_station_name)
        RESERVATION_STATION[reservation_station_name].ROBId = rob_name
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

def dequeueROB() -> None:
    for key in REORDER_BUFFER:
        if REORDER_BUFFER[key].ready:
            if REORDER_BUFFER[key].instruction != 'SW':
                REGISTER_STATUS[REORDER_BUFFER[key].destination].Qi = REORDER_BUFFER[key].value
            del REORDER_BUFFER[key]
            REORDER_BUFFER[key] = ROBEntry()
        else: break


def updateUnits() -> None:
    for key in RESERVATION_STATION:
        if RESERVATION_STATION[key].busy == True:
            if RESERVATION_STATION[key].timeToFinish == 0:
                rob_key = RESERVATION_STATION[key].ROBId
                REORDER_BUFFER[rob_key].ready = True
                REORDER_BUFFER[rob_key].leftReservationStation = True
                REORDER_BUFFER[rob_key].value = REORDER_BUFFER[rob_key].executeOperations(RESERVATION_STATION[REORDER_BUFFER[rob_key].reservationStation])
                dequeueROB()
                for sub_key in RESERVATION_STATION:
                    if RESERVATION_STATION[sub_key].Qj == key:
                        RESERVATION_STATION[sub_key].Qj = None
                        RESERVATION_STATION[sub_key].Vj = key
                    elif RESERVATION_STATION[sub_key].Qk == key:
                        RESERVATION_STATION[sub_key].Qk = None
                        RESERVATION_STATION[sub_key].Vk = key
                RESERVATION_STATION[key] = ReservationStation()
            else:
                if RESERVATION_STATION[key].Qj == None and RESERVATION_STATION[key].Qk == None:
                    RESERVATION_STATION[key].timeToFinish -= 1



def isReservationEmpty() -> bool:
    for chave in RESERVATION_STATION: 
        if RESERVATION_STATION[chave].busy == True:
            return False
    return True


def printInformation():
    print(f'---------------------------------------------- CLOCK {CLOCK} ----------------------------------------------')
    if len(INSTRUCTION_QUEUE) != 0:
        print(f'---------------------------------------------- INSTRUCTIONS QUEUE STATION ----------------------------------------------')
        for i in INSTRUCTION_QUEUE:
            print(str(i))
    
    if len(COMPLETE_INSTRUCTIONS) != 0:
        print(f'---------------------------------------------- COMPLETE INSTRUCTIONS STATION ----------------------------------------------')
        for i in COMPLETE_INSTRUCTIONS:
            print(str(i))

    print(f'---------------------------------------------- RESERVATION STATION ----------------------------------------------')
    for i in RESERVATION_STATION:
            print(str(i) + " " + str(RESERVATION_STATION[i]))

    print(f'---------------------------------------------- REGISTER STATUS ----------------------------------------------')
    for i in REGISTER_STATUS:
        print(str(i) + " " + str(REGISTER_STATUS[i]))

    print(f'---------------------------------------------- REORDER BUFFER ----------------------------------------------')
    for i in REORDER_BUFFER:
        print(str(i) + " " + str(REORDER_BUFFER[i]))
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
    readInstructions("instructions/instruction1.txt")
    loads_fu = 2
    store_fu = 2
    add_fu = 2
    mult_fu = 2
    createUnits(loads_fu, store_fu, add_fu, mult_fu)
    runProgram()

main()