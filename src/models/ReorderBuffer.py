from important_vars import (REGISTER_STATUS)

class ROBEntry:
    def __init__(self, instr: str, dest_reg: str) -> None:
        self.instr = instr  # armazena a instrução
        self.dest_reg = dest_reg  # armazena o registrador de destino
        self.value = None  # armazena o valor de saída
        self.ready = False  # indica se o valor está pronto para ser escrito no registrador

class ROB:
    def __init__(self, size):
        self.entries = [None] * size  # cria uma lista de entradas do tamanho especificado
        self.head = 0  # indica o próximo slot vazio do ROB
        self.tail = 0  # indica o slot da entrada mais antiga que ainda não foi gravada
    
    def insert(self, entry: ROBEntry) -> int:
        self.entries[self.head] = entry
        self.head = (self.head + 1) % len(self.entries)
        return (self.head - 1) % len(self.entries)

    def update(self, rob_idx: int, value: str) -> None:
        self.entries[rob_idx].value = value
    
    def has_false_dependencies(self, dest_reg: str) -> bool:
        for i in range(self.tail, self.head):
            entry = self.entries[i % len(self.entries)]
            if entry and not entry.ready and entry.dest_reg == dest_reg:
                return True
        return False
    
    def __str__(self):
        rob_str = "ROB:\n"
        for i, entry in enumerate(self.entries):
            if entry is None:
                rob_str += f"[{i}]: Empty\n"
            else:
                rob_str += f"[{i}]: {entry.instr}, Dest: {entry.dest_reg}, Value: {entry.value}, Ready: {entry.ready}\n"
        return rob_str