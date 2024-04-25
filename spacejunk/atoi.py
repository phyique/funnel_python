def atoi(s):
    rtr = 0
    for c in s:
        rtr = rtr * 10 + ord(c) - ord('0')
    return rtr


def to_str(index, t=[]):
    t.append(index)
    return t


state = to_str(5)
print(state)
state2 = to_str(50, [49])
print(state2)
state3 = to_str(500)
print(state3)
print(atoi("48923"))