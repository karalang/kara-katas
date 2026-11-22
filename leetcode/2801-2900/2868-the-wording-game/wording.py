# LeetCode #2868: The Wording Game -- the Python mirror of the ★ arm
# (wording.kara): each turn the largest word held of the letter in play
# if it beats the last word, else the largest of the next letter.


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


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def word(letters, longest):
    n = next_random() % longest + 1
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def deal(n, letters, longest):
    words = sorted(set(word(letters, longest) for _ in range(n)))
    while len(words) < 2:
        words = sorted(set(words + [word(letters, longest)]))
    a, b = [], []
    first = next_random() % len(words)
    for i, w in enumerate(words):
        if i == first or (next_random() % 2 == 0 and i != (first + 1) % len(words)):
            a.append(w)
        else:
            b.append(w)
    return a, b


def text(v):
    return "true" if v else "false"


def main():
    global seed
    print(
        f"{text(can_alice_win(['avokado', 'dabar'], ['brazil']))} {text(can_alice_win(['ananas', 'atlas', 'banana'], ['albatros', 'cikla', 'nogomet']))} {text(can_alice_win(['hrvatska', 'zastava'], ['bijeli', 'galeb']))}"
    )
    alice = [chr(ord("a") + 2 * i) for i in range(13)]
    bob = [chr(ord("a") + 2 * i + 1) for i in range(13)]
    print(text(can_alice_win(alice, bob)))
    seed = 2868
    wins = 0
    check = 0
    for c in range(3030):
        small = c < 3000
        if small:
            a, b = deal(next_random() % 7 + 2, 4, 3)
        else:
            a, b = deal(wide() % 90001 + 10000, 26 if c % 2 == 0 else 5, 8)
        win = can_alice_win(a, b)
        wins += win
        check = (check * 2 + (1 if win else 0)) % 1000000007
        if c == 2999:
            print(f"3000 small deals: Alice wins {wins}, checksum {check}")
            wins = 0
            check = 0
    print(f"30 large deals: Alice wins {wins}, checksum {check}")


main()
