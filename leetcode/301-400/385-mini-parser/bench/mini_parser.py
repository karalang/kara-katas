# Benchmark for #385: mirror of mini_parser.kara (recursive descent).


def deserialize(s):
    pos = [0]
    return parse_value(s, pos)


def parse_value(b, pos):
    if b[pos[0]] == "[":
        pos[0] += 1
        items = []
        if b[pos[0]] == "]":
            pos[0] += 1
            return items
        while True:
            items.append(parse_value(b, pos))
            if b[pos[0]] == ",":
                pos[0] += 1
            else:
                pos[0] += 1
                return items
    negative = False
    if b[pos[0]] == "-":
        negative = True
        pos[0] += 1
    n = 0
    while pos[0] < len(b) and b[pos[0]].isdigit():
        n = n * 10 + int(b[pos[0]])
        pos[0] += 1
    return -n if negative else n


def serialize(x):
    if isinstance(x, int):
        return str(x)
    return "[" + ",".join(serialize(i) for i in x) + "]"


def shape(x):
    if isinstance(x, int):
        return 0, 1, x
    depth = count = total = 0
    for item in x:
        d, c, s = shape(item)
        depth = max(depth, d)
        count += c
        total += s
    return depth + 1, count, total


def random_value(seed, depth):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    r = (seed[0] // 65536) % 10
    if depth == 0 or r < 4:
        seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
        return str((seed[0] // 65536) % 2000001 - 1000000)
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    n = (seed[0] // 65536) % 5
    return "[" + ",".join(random_value(seed, depth - 1) for _ in range(n)) + "]"


def main():
    seed = [385]
    s = "["
    while len(s) < 49000:
        if len(s) > 1:
            s += ","
        s += random_value(seed, 5)
    s += "]"
    checksum = 0
    P = 1000000007
    for _ in range(2000):
        x = deserialize(s)
        depth, count, total = shape(x)
        checksum = ((checksum * 31 + depth * 7 + count) % P + total % P + P) % P
    print(f"{len(s)} bytes parsed 2000 times, checksum {checksum}")


main()
