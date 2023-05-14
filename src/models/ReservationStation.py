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