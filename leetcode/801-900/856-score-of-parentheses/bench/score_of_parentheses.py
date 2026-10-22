# Benchmark for #856: Score of Parentheses -- the ★ arm, mirroring
# score_of_parentheses.kara.


def score_of_parentheses(s):
    stack = [0]
    for c in s:
        if c == '(':
            stack.append(0)
        else:
            inner = stack.pop()
            worth = 1 if inner == 0 else 2 * inner
            stack[-1] += worth
    return stack[0]


seed = 856


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 64, 4000000
    strings = []
    for g in range(count):
        s = []
        opens = balance = 0
        while len(s) < 50:
            if opens < 25 and (balance == 0 or next_random() % 4 < 1 + g % 3):
                s.append('(')
                opens += 1
                balance += 1
            else:
                s.append(')')
                balance -= 1
        strings.append(''.join(s))
    total = 0
    checksum = 0
    for round_ in range(rounds):
        k = score_of_parentheses(strings[round_ % count])
        total += k
        checksum = (checksum * 31 + k) % 1000000007
    print(f"{rounds} rounds of 64 strings: scores sum to {total}, checksum {checksum}")


main()
