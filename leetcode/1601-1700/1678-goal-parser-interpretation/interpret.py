# LeetCode #1678: Goal Parser Interpretation -- the Python mirror of the ★
# arm: one pass over the bytes.


def interpret(command):
    out = []
    i = 0
    while i < len(command):
        if command[i] == "G":
            out.append("G")
            i += 1
        elif command[i + 1] == ")":
            out.append("o")
            i += 2
        else:
            out.append("al")
            i += 4
    return "".join(out)


seed = 1678


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most):
    tokens = ["G", "()", "(al)"]
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        command = "".join(tokens[next_random() % 3] for _ in range(n))
        answer = interpret(command)
        total += len(answer)
        for c in answer:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"{count} commands of up to {most} tokens: {total} letters, checksum {check}")


print(interpret("G()(al)"))
print(interpret("G()()()()(al)"))
print(interpret("(al)G(al)()()G"))
print(interpret("G"))
print(interpret("()"))
print(interpret("(al)"))
batch(3000, 10)
batch(300, 50)
batch(30, 10000)
