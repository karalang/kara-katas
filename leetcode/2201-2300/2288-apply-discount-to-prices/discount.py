# LeetCode #2288: Apply Discount to Prices -- the Python mirror of the ★
# arm, `discount.kara`.


def is_price(word):
    return len(word) > 1 and word.startswith("$") and all(c in "0123456789" for c in word[1:])


def discount_prices(sentence, discount):
    words = []
    for word in sentence.split(" "):
        if is_price(word):
            price = int(word[1:])
            cents = price * (100 - discount)
            words.append(f"${cents // 100}.{cents % 100:02d}")
        else:
            words.append(word)
    return " ".join(words)


# ---- test harness ---------------------------------------------------------

seed = 2288


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word():
    kind = next_random() % 8
    length = next_random() % 10 + 1
    w = ""
    if kind < 4 or kind == 5:
        w += "$"
    if kind == 4:
        return "$"
    for i in range(length):
        digit = chr(ord("0") + next_random() % 10)
        letter = chr(ord("a") + next_random() % 26)
        if kind < 4 or kind == 7:
            w += digit
        elif kind == 5 and i == length - 1:
            w += "e"
        elif kind == 5:
            w += digit
        else:
            w += letter
    return w


def main():
    cases = [
        ("there are $1 $2 and 5$ candies in the shop", 50),
        ("1 2 $3 4 $5 $6 7 8$ $9 $10$", 100),
        ("$0 $00 $007", 37),
        ("$9999999999 $1000000000", 1),
        ("$9999999999 $1000000000", 99),
        ("$ $$5 $5$ $5e3 a$1", 10),
        ("x $1234567890 y", 0),
    ]
    for sentence, discount in cases:
        print(f"{discount}: {discount_prices(sentence, discount)}")
    check = 0
    length = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        discount = next_random() % 101
        words = [word() for _ in range(n)]
        answer = discount_prices(" ".join(words), discount)
        for b in answer.encode():
            check = (check * 31 + b) % 1000000007
        length += len(answer)
    print(f"2000 sentences: checksum {check}, {length} bytes")


main()
