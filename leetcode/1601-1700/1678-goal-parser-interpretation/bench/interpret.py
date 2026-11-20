# LeetCode #1678: Goal Parser Interpretation -- the bench's Python mirror:
# the ★ arm on 100000 random commands of up to 100 characters, all drawn
# first, each interpreted 20 times.


def interpret(command):
    out = []
    i = 0
    n = len(command)
    while i < n:
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


def main():
    count, rounds = 100000, 20
    tokens = ["G", "()", "(al)"]
    commands = []
    for _ in range(count):
        command = ""
        length = next_random() % 100 + 1
        while True:
            token = tokens[next_random() % 3]
            if len(command) + len(token) > length:
                break
            command += token
        if not command:
            command = "G"
        commands.append(command)
    total = 0
    check = 0
    for r in range(rounds):
        for command in commands:
            answer = interpret(command)
            n = len(answer)
            total += n
            check = (check * 31 + n + ord(answer[-1]) + r) % 1000000007
    print(f"{count} commands, {rounds} rounds: {total} letters, checksum {check}")


main()
