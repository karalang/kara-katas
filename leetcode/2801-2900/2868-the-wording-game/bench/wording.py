# LeetCode #2868: The Wording Game -- the bench, as wording.kara: 20
# deals of 10^5 words, each played 20 times by the table arm.

def table(words):
    top = [-1] * 26
    for i, w in enumerate(words):
        top[ord(w[0]) - ord("a")] = i
    return top


def can_alice_win(a, b):
    last = a[0]
    tops = [table(a), table(b)]
    hands = [a, b]
    turn = 1
    while True:
        c = ord(last[0]) - ord("a")
        same = tops[turn][c]
        if same >= 0 and hands[turn][same] > last:
            last = hands[turn][same]
        elif c < 25 and tops[turn][c + 1] >= 0:
            last = hands[turn][tops[turn][c + 1]]
        else:
            return turn == 1
        turn = 1 - turn


seed = 2868


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def deal(n, letters, longest):
    words = []
    for _ in range(n):
        ln = next_random() % longest + 1
        words.append("".join(chr(ord("a") + next_random() % letters) for _ in range(ln)))
    words = sorted(set(words))
    a, b = [], []
    first = next_random() % len(words)
    for i, w in enumerate(words):
        if i == first or (next_random() % 2 == 0 and i != (first + 1) % len(words)):
            a.append(w)
        else:
            b.append(w)
    return a, b


def main():
    count, rounds, n = 20, 20, 100000
    deals = [deal(n, 26 if c % 2 == 0 else 5, 8) for c in range(count)]
    wins = 0
    check = 0
    for r in range(rounds):
        for a, b in deals:
            win = can_alice_win(a, b)
            wins += win
            check = (check * 2 + r + (1 if win else 0)) % 1000000007
    print(f"{count} deals of {n} words, {rounds} rounds: Alice wins {wins}, checksum {check}")


main()
