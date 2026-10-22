# LeetCode #856: Score of Parentheses -- Python mirror of the ★ arm (a
# stack of the scores of the groups still open).


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


def show(s):
    print(f'"{s}" -> {score_of_parentheses(s)}')


seed = 856


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(pairs):
    s = []
    opens = 0
    balance = 0
    while len(s) < 2 * pairs:
        if opens < pairs and (balance == 0 or next_random() % 2 == 0):
            s.append('(')
            opens += 1
            balance += 1
        else:
            s.append(')')
            balance -= 1
    return ''.join(s)


def all_strings(pairs, prefix, opens, closes, out):
    if closes == pairs:
        out.append(prefix)
        return
    if opens < pairs:
        all_strings(pairs, prefix + '(', opens + 1, closes, out)
    if closes < opens:
        all_strings(pairs, prefix + ')', opens, closes + 1, out)


def main():
    show("()")
    show("(())")
    show("()()")
    show("(()(()))")
    show("((()))")
    show("(()())")
    show("()(())")
    show("((())())()")
    show("((((((((((((((((((((((((()))))))))))))))))))))))))")
    show("()()()()()()()()()()()()()()()()()()()()()()()()()")
    show("(((((((((((((((((((((((())))))))))))))))))))))))()")
    every = []
    for pairs in range(1, 9):
        all_strings(pairs, '', 0, 0, every)
    every_total = sum(score_of_parentheses(s) for s in every)
    print(f"all {len(every)} balanced strings of 1 to 8 pairs: scores sum to {every_total}")
    total = 0
    check = 0
    for _ in range(300):
        s = random_string(1 + next_random() % 25)
        k = score_of_parentheses(s)
        total += k
        check = (check * 31 + k) % 1000000007
    print(f"300 random strings of up to 25 pairs: scores sum to {total}, checksum {check}")


main()
