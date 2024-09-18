from t_machine import E, R, L, S
from t_machine import sigma, transitions
from t_machine import run


letters = 'a', 'b', 'c',
sigma.update(*letters)


translate_table = {
    'a': ('a', 'c'),
    'b': (E,),
    'c': ('b', 'c'),
}


def q_with_l(t_act, q, *args, **kwargs):
    for l in letters:
        yield from t_act(q+l, *args, **kwargs)


def t_read(q, *sumbols, M=R):
    for s in sumbols:
        yield (q, s), (q+s, E, M)


def t_move(q, signal=E, *signals, M=R):
    missed = sigma - {signal, *signals}
    for s in missed:
        yield (q, s), (q, s, M)


def t_switch_mode(q, mode, signal=E, *signals, M=R, old_mode=''):
    for s in signal, *signals:
        yield (old_mode+q, s), (mode+q, s, M)


def t_markup(ql, M=R):
    q, l = ql[:-1], ql[-1]
    n = len(translate_table[l])
    prev_q = ql
    for i in range(n-1):
        next_q = ql+str(i)
        yield (prev_q, E), (next_q, l, M)
        prev_q = next_q
    yield (prev_q, E), (q, l, -M)
    


def t_mode_translate(q, M=R):
    for l in letters:
        prev_q = q
        w = translate_table[l]
        for i, s in enumerate(w[:-1]):
            next_q = q+l+str(i)
            yield (prev_q, l), (next_q, s, M)
            prev_q = next_q
        yield (prev_q, l), (q, w[-1], M)
        


def t_mode_markup():
    # Try start read
    yield from t_switch_mode('', 'r', *letters, M=S)
    
    # Read letter
    yield from t_read('r', *letters)
    yield from q_with_l(t_move, 'r')
    
    # Go end and mark up for translation of letter
    yield from q_with_l(t_switch_mode, '', 'm', old_mode='r')
    yield from q_with_l(t_move, 'm')
    yield from q_with_l(t_markup, 'm')
    yield from t_move('m', M=L)
    
    # Return to initial
    yield from t_switch_mode('', 'i', M=L, old_mode='m')
    yield from t_move('i', M=L)
    yield from t_switch_mode('', '', old_mode='i')
    
    # Translate on murked
    yield from t_switch_mode('', 't')
    yield from t_mode_translate('t')
    
    # Exit at the end
    yield ('t', E), (0, E, S)


transitions.update(
    t_mode_markup()
)

input_str = "abc"
print(''.join(run([*input_str])))

