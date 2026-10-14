# Benchmark for #591: Python mirror of the ★ arm (one scan with a stack
# of open tags); see tag_validator.kara.


def valid_name(name):
    return 1 <= len(name) <= 9 and all("A" <= c <= "Z" for c in name)


def is_valid(code):
    n = len(code)
    stack = []
    i = 0
    while i < n:
        if i > 0 and not stack:
            return False
        if code.startswith("<![CDATA[", i):
            if not stack:
                return False
            k = code.find("]]>", i + 9)
            if k < 0:
                return False
            i = k + 3
        elif code.startswith("</", i):
            start = i + 2
            k = code.find(">", start)
            if k < 0:
                return False
            name = code[start:k]
            if not stack or stack[-1] != name:
                return False
            stack.pop()
            i = k + 1
        elif code.startswith("<", i):
            start = i + 1
            k = code.find(">", start)
            if k < 0:
                return False
            name = code[start:k]
            if not valid_name(name):
                return False
            stack.append(name)
            i = k + 1
        else:
            if not stack:
                return False
            i += 1
    return not stack


# ---- benchmark ---------------------------------------------------------------


def main():
    seed = 591

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    names = ["A", "XY", "ABCDEFGHI", "CODE"]
    texts = ["x", " ", ">", "]]>", "!", "[", "y", "/", "...", "<![CDATA[<A>]]>"]

    def snippet(depth):
        name = names[step() % len(names)]
        out = f"<{name}>"
        parts = step() % 7
        for _ in range(parts):
            if step() % 10 < 4 and depth > 0:
                out += snippet(depth - 1)
            else:
                out += texts[step() % len(texts)]
        if step() % 40 == 0:
            out += "</B>"
        else:
            out += f"</{name}>"
        return out

    count = 1000
    rounds = 1000
    codes = []
    while len(codes) < count:
        code = snippet(4)
        if 200 <= len(code) <= 500:
            codes.append(code)
    valid = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            if is_valid(codes[(rnd * 7 + g) % count]):
                valid += 1
                checksum = (checksum * 31 + g + 1) % 1000000007
    print(f"{count} snippets, {rounds} rounds: {valid} valid, checksum {checksum}")


main()
