import json


def readDFA(path):
    f = open(path, "r")
    DFA = json.load(f)
    return DFA


def initializeMatrix(DFA, n):
    states = {}
    i = 0
    for st in sorted(DFA['states']):
        states[st] = i
        i += 1

    s = []
    for st in DFA['start_states']:
        s.append(states[st])

    f = []
    for st in DFA['final_states']:
        f.append(states[st])

    m = [[None] * n for _ in range(n)]

    for trans in DFA['transition_function']:
        u = states[trans[0]]
        v = states[trans[2]]
        m[u][v] = trans[1]

    return s, f, m


def add(a, b):
    if a is None and b is None:
        return None
    if a is None:
        return b
    if b is None:
        return a
    if a == b:
        return a
    if a == 'e' and len(b) > 1 and (b[0] == 'e' or b[-1] == 'e'):
        return 'e'
    if b == 'e' and len(a) > 1 and (a[0] == 'e' or a[-1] == 'e'):
        return 'e'

    return '(' + ' V '.join([a, b]) + ')'


def mul(a, b, c):
    if a is None or c is None:
        return None
    if a == 'e' and b == 'e' and c == 'e':
        return 'e'
    res = ''
    if a != 'e':
        res += a
    if b != 'e':
        res += '{' + b + '}'
    if c != 'e':
        res += c
    return res


def convertToRegex(DFA):
    n = len(DFA['states'])

    s, f, m = initializeMatrix(DFA, n)

    c = [[[None] * n for i in range(n)] for j in range(n + 1)]

    for i in range(n):
        for j in range(n):
            c[0][i][j] = m[i][j]

    for i in range(n):
        c[0][i][i] = add('e', c[0][i][i])

    for k in range(n):
        for i in range(n):
            for j in range(n):
                c[k + 1][i][j] = add(c[k][i][j], mul(c[k][i][k], c[k][k][k], c[k][k][j]))

    res = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            res[i][j] = c[n][i][j]

    ans = ''
    k = 0
    for i in s:
        for j in f:
            if k != 0:
                ans += ' V ' + res[i][j]
            else:
                ans = res[i][j]
            k += 1

    return ans


def main():
    DFA = readDFA('test.json')
    regex = convertToRegex(DFA)
    print(regex)

if __name__ == "__main__":
    main()
