CLOCK_TIME_INSTRUCTION = {"LW": 2, "SW": 2, "ADD": 4, "SUB": 2, "MUL": 2, "DIV": 4}
INSTRUCTION_QUEUE = []
RESERVATION_STATION = {}
REGISTER_STATUS = {}
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

    def __str__(self) -> str:
        return "[Time to finish: " + str(self.timeToFinish) + ", Busy: " + str(self.busy) + ", Op: " + str(self.op) + ", Destination: " + str(self.D) + ", Vj: " + str(self.Vj) + ", Vk: " + str(
            self.Vk) + ", Qj: " + str(self.Qj) + ", Qk: " + str(self.Qk) + ", A: " + str(self.A) + "]"
    
class ROBEntry:
    def __init__(self, instruction: InstructionUnit, destination: str):
        self.instruction = instruction
        self.destination = destination
        self.value = None
        self.ready = False

class ROB:
    def __init__(self, size: int):
        self.size = size
        self.buffer = [None] * size
        self.head = 0
        self.tail = 0

    def is_full(self) -> bool:
        return (self.tail + 1) % self.size == self.head

    def is_empty(self) -> bool:
        return self.tail == self.head

    def enqueue(self, instruction: InstructionUnit, destination: str) -> bool:
        if self.is_full():
            return False

        self.buffer[self.tail] = ROBEntry(instruction, destination)
        self.tail = (self.tail + 1) % self.size
        return True

    def dequeue(self) -> ROBEntry:
        if self.is_empty():
            return None

        entry = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.size
        return entry

    def __str__(self):
        rob_str = "---------------------------------------------- ROB ----------------------------------------------\n"
        for i, buffer in enumerate(self.buffer):
            if buffer is None:
                rob_str += f"[{i}]: Empty\n"
            else:
                rob_str += f"[{i}]: {buffer.instr}, Dest: {buffer.dest_reg}, Value: {buffer.value}, Ready: {buffer.ready}\n"
        return rob_str

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

def executeOperations(instruction_reservation: ReservationStation) -> str:
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

def updateUnits() -> None:
    for chave in RESERVATION_STATION:
        if RESERVATION_STATION[chave].busy == True:
            if RESERVATION_STATION[chave].timeToFinish == 0:
                REGISTER_STATUS[RESERVATION_STATION[chave].D].Qi = executeOperations(RESERVATION_STATION[chave])
                for sub_chave in RESERVATION_STATION:
                    if RESERVATION_STATION[sub_chave].Qj == chave:
                        RESERVATION_STATION[sub_chave].Qj = None
                        RESERVATION_STATION[sub_chave].Vj = chave
                    elif RESERVATION_STATION[sub_chave].Qk == chave:
                        RESERVATION_STATION[sub_chave].Qk = None
                        RESERVATION_STATION[sub_chave].Vk = chave
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
    readInstructions("instructions/instruction1.txt")
    loads_fu = 3
    store_fu = 3
    add_fu = 3
    mult_fu = 3
    createUnits(loads_fu, store_fu, add_fu, mult_fu)
    runProgram()

main()