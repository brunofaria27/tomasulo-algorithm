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
    
    def insert(self, instr: str, dest_reg: str) -> int:
        # cria uma nova entrada do ROB
        entry = ROBEntry(instr, dest_reg)
        # adiciona a entrada na próxima posição vazia do ROB
        self.entries[self.head] = entry
        # atualiza o ponteiro para a próxima posição vazia
        self.head = (self.head + 1) % len(self.entries)
        # retorna o índice da nova entrada do ROB
        return (self.head - 1) % len(self.entries)

    def update(self, rob_idx: int, value: str) -> None:
        # atualiza o valor da entrada do ROB
        self.entries[rob_idx].value = value

    def has_false_dependencies(self, dest_reg: str) -> bool:
        # verifica se há dependências falsas em relação ao registrador de destino fornecido
        for i in range(self.tail, self.head):
            entry = self.entries[i % len(self.entries)]
            if entry and not entry.ready and entry.dest_reg == dest_reg:
                return True
        return False