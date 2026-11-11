# LeetCode #1111: Maximum Nesting Depth of Two Valid Parentheses Strings
# -- the bench's Python mirror: the ★ arm over the same 16 strings and
# the same valid prefixes.


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


seed = 1111


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_vps(pairs):
    out = []
    cuts = []
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
            if depth == 0:
                cuts.append(len(out))
    return "".join(out), cuts


def main():
    strings = [random_vps(5000) for _ in range(16)]
    chars = 0
    ones = 0
    check = 0
    for rnd in range(1000):
        for j in range(len(strings)):
            s, cuts = strings[j]
            cut = cuts[(rnd * 7919 + j * 104729) % len(cuts)]
            answer = max_depth_after_split(s[:cut])
            chars += cut
            ones += sum(answer)
            check = (check * 31 + answer[(rnd * 31 + j) % cut]) % 1000000007
    print(f"1000 rounds over 16 strings of 10000 characters: {chars} characters, {ones} in the second group, checksum {check}")


main()
