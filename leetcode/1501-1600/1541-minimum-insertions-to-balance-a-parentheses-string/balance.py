# LeetCode #1541: Minimum Insertions to Balance a Parentheses String --
# Python mirror of balance.kara (the ★ arm, one pass keeping the ')' still
# wanted); its output is byte-identical.


def min_insertions(s):
    inserted = 0
    need = 0
    for c in s:
        if c == "(":
            if need % 2 == 1:
                inserted += 1
                need -= 1
            need += 2
        else:
            need -= 1
            if need < 0:
                inserted += 1
                need = 1
    return inserted + need


seed = 1541


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    for _ in range(count):
        a = next_random()
        n = (a * 32768 + next_random()) % most + 1
        chance = next_random() % 101
        s = "".join("(" if next_random() % 100 < chance else ")" for _ in range(n))
        check = mix(check, min_insertions(s))
    print(f"{count} strings of up to {most} parentheses: checksum {check}")


def main():
    examples = ["(()))", "())", "))())(", "((((((", ")))))))", "(", ")", "()", "())())", ")()", "(()))(()))))"]
    for s in examples:
        print(f"{s} -> {min_insertions(s)}")
    print(f"100000 '(' -> {min_insertions('(' * 100000)}")
    print(f"100000 ')' -> {min_insertions(')' * 100000)}")
    print(f"33333 '())' -> {min_insertions('())' * 33333)}")
    batch(3000, 12)
    batch(300, 1000)
    batch(30, 100000)


main()
