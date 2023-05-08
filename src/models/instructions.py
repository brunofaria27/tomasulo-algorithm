from important_vars import CLOCK_TIME_INSTRUCTION

class InstructionUnit:
    def __init__(self, operation: str, register: str, arg1: str, arg2: str) -> None:
        self.operation = operation
        self.register = register
        self.arg1 = arg1
        self.arg2 = arg2
        self.clocks = CLOCK_TIME_INSTRUCTION[operation]
        self.clocksLeft = CLOCK_TIME_INSTRUCTION[operation]

    def printInstruction(self) -> None:
        return "Operation: " + str(self.operation) + " - Register: " + str(self.register) + " - Argument 1: " + str(self.arg1) + " - Argument 2: " + str(self.arg2) + " - Clocks: " + str(
                self.clocks) + " - Clocks left: " + str(self.clocksLeft)