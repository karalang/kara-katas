# LeetCode #2288: Apply Discount to Prices -- the bench, the ★ arm's
# Python mirror. Split on spaces; a `$` and then only digits is a price,
# discounted in whole cents and written back with two decimals.


def is_price(word):
    return len(word) > 1 and word.startswith("$") and all(48 <= b <= 57 for b in word[1:].encode())


def discount_prices(sentence, discount):
    words = []
    for word in sentence.split(" "):
        if is_price(word):
            cents = int(word[1:]) * (100 - discount)
            words.append(f"${cents // 100}.{cents % 100:02}")
        else:
            words.append(word)
    return " ".join(words)


# ---- bench harness ---------------------------------------------------------

seed = 2288


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word():
    kind = next_random() % 4
    length = next_random() % 8 + 1
    w = "$" if kind < 2 else ""
    for _ in range(length):
        r = next_random()
        w += chr(48 + r % 10) if kind == 0 or kind == 3 else chr(97 + r % 26)
    return w


def main():
    sentences = [" ".join(word() for _ in range(12)) for _ in range(4000)]
    check = 0
    for p in range(50):
        for sentence in sentences:
            answer = discount_prices(sentence, p * 2)
            check = (check * 31 + len(answer) + answer.encode()[len(answer) - 2]) % 1000000007
    print(f"50 passes over 4000 sentences: checksum {check}")


main()
