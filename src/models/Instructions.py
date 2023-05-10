from important_vars import CLOCK_TIME_INSTRUCTION

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