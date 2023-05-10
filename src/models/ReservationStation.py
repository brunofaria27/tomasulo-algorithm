class ReservationStation:
    def __init__(self, name: str) -> None:
        self.name = name
        self.busy = False
        self.op = None
        self.D = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None # Only used in LW and SW

    def __str__(self) -> str:
        return "[Name: " + str(self.name) + ", Busy: " + str(self.busy) + ", Op: " + str(self.op) + ", Destination: " + str(self.D) + ", Vj: " + str(self.Vj) + ", Vk: " + str(
            self.Vk) + ", Qj: " + str(self.Qj) + ", Qj: " + str(self.Qj) + ", A: " + str(self.A) + "]"