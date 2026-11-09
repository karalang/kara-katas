# LeetCode #2042: Check if Numbers Are Ascending in a Sentence -- the ★ arm
# in Python, the same algorithm and workload as ascending.kara: the sentence
# split at its spaces, each token that parses compared with the last.


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
    sentences = [sentence() for _ in range(1000)]
    calls = ascending = check = 0
    for rnd in range(1000):
        for i, s in enumerate(sentences):
            answer = are_numbers_ascending(s)
            calls += 1
            if answer:
                ascending += 1
                check = (check * 31 + rnd + i) % 1000000007
    print(f"{calls} calls: {ascending} ascending, checksum {check}")


main()
