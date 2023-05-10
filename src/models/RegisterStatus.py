class RegisterStatus:
    def __init__(self, field) -> None:
        self.field = field
        self.Qi = None
    
    def __str__(self) -> str:
        return "[Field: " + str(self.field) + ", Qi: " + str(self.Qi) + "]"
    