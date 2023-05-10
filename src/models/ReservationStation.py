class ReservationStation:
    def __init__(self):
        self.busy = False
        self.exec = None
        self.op = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None # Only used in LW and SW