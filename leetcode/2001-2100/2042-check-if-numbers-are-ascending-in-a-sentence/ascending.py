# LeetCode #2042: Check if Numbers Are Ascending in a Sentence -- Python
# mirror of the ★ arm (ascending.kara): the sentence split at its spaces,
# each token that parses as an integer compared with the last.


def are_numbers_ascending(s):
    last = 0
    for token in s.split(" "):
        try:
            n = int(token)
        except ValueError:
            continue
        if n <= last:
            return False
        last = n
    return True


# ---- test harness ---------------------------------------------------------

seed = 2042


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sentence():
    words = 1 + next_random() % 30
    climb = next_random() % 20 + 1
    drift = next_random() % 4
    last = next_random() % 10 + 1
    tokens = []
    numbers = 0
    length = 0
    for t in range(words + 2):
        if t >= words or next_random() % 3 == 0:
            last = min(max(last + next_random() % (climb + drift + 1) - drift, 1), 99)
            numbers += 1
            token = str(last)
        else:
            token = ""
            for _ in range(next_random() % 6 + 1):
                token += "abcxyz"[next_random() % 6]
        if length + len(token) + 1 > 200 and numbers >= 2:
            break
        length += len(token) + 1
        tokens.append(token)
    return " ".join(tokens)


def main():
    examples = [
        "1 box has 3 blue 4 red 6 green and 12 yellow marbles",
        "hello world 5 x 5",
        "sunset is at 7 51 pm overnight lows will be in the low 50 and 60 s",
        "1 2",
        "2 1",
        "a 9 b 10 c 99",
        "a 10 b 9",
        "99 x 98 y",
        "4 4",
    ]
    for s in examples:
        print(f'"{s}" -> {"true" if are_numbers_ascending(s) else "false"}')
    ascending = 0
    check = 0
    for _ in range(4000):
        answer = are_numbers_ascending(sentence())
        if answer:
            ascending += 1
        check = (check * 31 + (2 if answer else 1)) % 1000000007
    print(f"4000 sentences: {ascending} ascending, checksum {check}")


main()
