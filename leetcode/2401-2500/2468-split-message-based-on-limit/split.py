def digits(v):
    return len(str(v))


def split_message(message, limit):
    n = len(message)
    digit_sum = 0
    parts = 0
    b = 1
    while 3 + 2 * digits(b) < limit:
        digit_sum += digits(b)
        if b * (limit - 3 - digits(b)) - digit_sum >= n:
            parts = b
            break
        b += 1
    out = []
    if parts == 0:
        return out
    at = 0
    for a in range(1, parts + 1):
        room = limit - 3 - digits(a) - digits(parts)
        end = min(at + room, n)
        out.append(f"{message[at:end]}<{a}/{parts}>")
        at = end
    return out


# ---- test harness ---------------------------------------------------------

seed = 2468


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_message(n):
    letters = "abcdefghijklmnopqrstuvwxyz "
    text = []
    for _ in range(n):
        at = next_random() % 27
        text.append(letters[at])
    return "".join(text)


def fold(parts):
    check = len(parts)
    for part in parts:
        for c in part:
            check = (check * 31 + ord(c)) % 1000000007
    return check


def show(parts):
    return "[" + ", ".join(parts) + "]"


def main():
    cases = [
        ("this is really a very awesome message", 9),
        ("short message", 15),
        ("abc", 9),
        ("abc", 5),
        ("a" * 68, 7),
        ("hello", 7),
        ("abcdefghij", 6),
        ("abcdefghijk", 7),
        ("abcdefghijklmnopqrstuvwxyz " * 5 + "ab", 20),
    ]
    for message, limit in cases:
        print(f"\"{message}\", {limit} -> {show(split_message(message, limit))}")
    long = random_message(10000)
    for limit in (6, 11, 12, 100, 10000):
        parts = split_message(long, limit)
        print(f"10^4 letters, limit {limit}: {len(parts)} parts, checksum {fold(parts)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 300
        message = random_message(n)
        limit = 1 + next_random() % 40
        check = (check * 31 + fold(split_message(message, limit))) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
