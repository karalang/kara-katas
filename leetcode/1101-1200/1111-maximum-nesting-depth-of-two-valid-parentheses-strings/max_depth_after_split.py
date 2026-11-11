# LeetCode #1111: Maximum Nesting Depth of Two Valid Parentheses Strings
# -- the Python mirror of the ★ arm, a depth counter: each pair goes to
# the group of its depth's parity. Prints the same lines as every Kāra arm.


def max_depth_after_split(seq):
    depth = 0
    answer = []
    for c in seq:
        if c == "(":
            answer.append(depth % 2)
            depth += 1
        else:
            depth -= 1
            answer.append(depth % 2)
    return answer


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_vps(pairs):
    out = []
    opens = 0
    depth = 0
    while opens < pairs or depth > 0:
        if opens < pairs and (depth == 0 or next_random() % 2 == 0):
            out.append("(")
            opens += 1
            depth += 1
        else:
            out.append(")")
            depth -= 1
    return "".join(out)


def fold(h, answer):
    for g in answer:
        h = (h * 3 + g + 1) % 1000000007
    return h


def main():
    global seed
    cases = ["(()())", "()(())()", "()", "(())", "((()))", "()()()", "(()(()))", "((())())(())", "(((())))()", "()((()))(()())"]
    for seq in cases:
        print(f"{seq} -> [{', '.join(map(str, max_depth_after_split(seq)))}]")
    seed = 1111
    ones = 0
    check = 0
    for _ in range(2000):
        pairs = next_random() % 50 + 1
        seq = random_vps(pairs)
        answer = max_depth_after_split(seq)
        ones += sum(answer)
        check = fold(check, answer)
    print(f"2000 random strings: {ones} in the second group, checksum {check}")
    nest = "(" * 5000 + ")" * 5000
    answer = max_depth_after_split(nest)
    print(f"5000 nested pairs: {sum(answer)} in the second group, checksum {fold(0, answer)}")
    seq = random_vps(5000)
    answer = max_depth_after_split(seq)
    print(f"5000 random pairs: {sum(answer)} in the second group, checksum {fold(0, answer)}")


main()
