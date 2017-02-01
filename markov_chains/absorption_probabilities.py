import fractions

def row_multiply(factor, row):
    return map(lambda x: factor * x, row)

def row_add(row1, row2):
    res = []
    for i in range(0, len(row1)):
        res.append(row1[i] + row2[i])
    return res

def setup_equation_matrix(m, terminal_states):
    # assume the terminal states are ordered after
    equations = []
    for row, transitions in enumerate(m):
        # equations are of the form: a_i = a_p0 + a_p1 + a_p2... or
        # a_i - a_p0 - a_p1 = a_sn1 + a_sn2 + ...
        if row in terminal_states:
            continue
        state_equation = []
        p_sum = sum(transitions)
        for index, p in enumerate(transitions):
            if index == row:
                if p == 0:
                    state_equation.append(1*p_sum)
                else:
                    state_equation.append(p_sum - p)
            elif index in terminal_states:
                state_equation.append(p)
            else:
                state_equation.append(p * -1)
        equations.append(state_equation)
    # simultaneous equations are normalized
    return equations

def row_reduction(equation_matrix, terminal_states):
    # We need to obtain the solution for row 0, as we always start in S0
    eqn = 0
    for i in range(1, len(equation_matrix[0])):
        if i in terminal_states:
            continue
        eqn += 1
        for k in range(0, len(equation_matrix)):
            if k == eqn:
                continue
            eliminated = equation_matrix[k][i]
            added_val = equation_matrix[eqn][i]
            equation_matrix[k] = row_multiply(abs(added_val),
                                              equation_matrix[k])
            if eliminated*added_val < 0:
                added_row = row_multiply(abs(eliminated),
                                         equation_matrix[eqn])
            else:
                added_row = row_multiply(abs(eliminated)*-1,
                                         equation_matrix[eqn])
            equation_matrix[k] = row_add(equation_matrix[k], added_row)

def print_matrix(m):
    for row in m:
        print row

def get_terminal_states(m):
    terminal_states = []
    for index, transitions in enumerate(m):
        if sum(transitions) == 0:
            terminal_states.append(index)
    return terminal_states

#matrix = [
#    [0, 1, 0, 0, 0, 1], #s0
#    [4, 0, 0, 3, 2, 0], #s1
#    [0, 0, 0, 0, 0, 0], #s2
#    [0, 0, 0, 0, 0, 0], #s3
#    [0, 0, 0, 0, 0, 0], #s4
#    [0, 0, 0, 0, 0, 0]  #s5
#]

#matrix = [
#    [0, 2, 1, 0, 0],
#    [0, 0, 0, 3, 4],
#    [0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0]
#]
#
#matrix = [
#    [0, 1, 2, 0, 0],
#    [0, 0, 0, 0, 0],
#    [0, 0, 0, 3, 4],
#    [0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0]
#]

#matrix = [
#    [0, 2, 2],
#    [2, 0, 2],
#    [0, 0, 0],
#]

#matrix = [
#    [0, 0, 0, 0, 0]
#]

#matrix = [
#    [0, 6, 0, 0, 4, 0],
#    [0, 0, 5, 0, 5, 0],
#    [0, 0, 0, 4, 6, 0],
#    [0, 0, 0, 0, 7, 3],
#    [0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0]
#]

#matrix = [
#    [0, 4, 0, 6, 0, 0],
#    [0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0],
#    [0, 5, 0, 0, 5, 0],
#    [0, 6, 0, 0, 0, 4],
#    [0, 7, 3, 0, 0, 0]
#]

matrix = [
    [0, 2, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 5, 0, 5, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0]
]

matrix = [
 [1, 2, 3, 0, 0, 0],
 [4, 5, 6, 0, 0, 0],
 [7, 8, 9, 1, 0, 0],
 [0, 0, 0, 0, 1, 2],
 [0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0]
]

def reduce_fractions(numerators, denominator):
    gcd = denominator
    for n in numerators:
        gcd = fractions.gcd(n, gcd)
    result = map(lambda x: int(x/gcd), numerators)
    result.append(int(denominator/gcd))
    return result

def answer(m):
    terminal_states = get_terminal_states(matrix)
    eqns = setup_equation_matrix(matrix, terminal_states)
    if not eqns:
        result = [0 for i in terminal_states]
        return result + [0]
    print eqns
            
    row_reduction(eqns, terminal_states)
    result = []
    for i in range(0, len(eqns[0])):
        if i in terminal_states:
            result.append(eqns[0][i])
    return reduce_fractions(result, eqns[0][0])

print answer(matrix)
