E = ' '

sigma = {
    E,
}

L = -1
R = +1
S = 0


transitions = {
}


def get_cell(tape, ltape, head):
    if head < 0:
        head = -head - 1
        tape = ltape
    if head < len(tape):
        return tape[head]
    return E


def set_cell(tape, ltape, head, s):
    if head < 0:
        head = -head - 1
        tape = ltape
    if (d:=head-len(tape)+1) > 0:
        tape.extend([E]*d)
    tape[head] = s

def get_operation(q, s):
    return transitions[q, s]


def run(tape, ltape=None):
    ltape = ltape or []
    head = 0
    q = ''
    while q != 0:
        s = get_cell(tape, ltape, head)
        q, s, m = get_operation(q, s)
        set_cell(tape, ltape, head, s)
        head += m
    ltape.reverse()
    return ltape + tape

