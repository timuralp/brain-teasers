# Compute XOR of a list of numbers, starting with "start" and of length
# "length". The list is defined as follows, for length of 5, starting at 10:
# 10 11  12  13  14
# 15 16  17  18  #19
# 20 21  22  #23 24
# 25 26  #27 28  29
# 30 #31 32  33  34
#
# So, the goal is to compute XOR of:
# 10 11 12 13 14 15 16 17 18 20 21 22 25 26 30

def answer(start, length):
    table = [lambda x: 0, lambda x: x-1, lambda x: 1, lambda x: x]

    # compute the start/end for each line
    xor = 0
    for i in range(0, length):
        line_start = start + i * length
        line_end = line_start + length - i
        line_xor = table[line_start%4](line_start) ^ table[line_end%4](line_end)
        xor = xor ^ line_xor
    return xor
