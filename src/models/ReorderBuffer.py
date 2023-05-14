from models.ReservationStation import ReservationStation

class ROBEntry:
    def __init__(self):
        self.instruction = None
        self.destination = None
        self.value = None
        self.ready = False
        self.reservationStation = None

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
        return f"[Instruction: {self.instruction}, Destination: {self.destination}, Ready: {self.ready}, Value: {self.value}, Reservation Station name: {self.reservationStation}]"