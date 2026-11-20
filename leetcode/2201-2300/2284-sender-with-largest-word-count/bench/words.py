# LeetCode #2284: Sender With Largest Word Count -- the bench, the ★
# arm's Python mirror. A dict of totals, then the largest by total and
# name.


def largest_word_count(messages, senders):
    totals = {}
    for message, sender in zip(messages, senders):
        words = len(message.split(" "))
        totals[sender] = totals.get(sender, 0) + words
    best = ""
    most = 0
    for sender, total in totals.items():
        if total > most or (total == most and sender > best):
            best = sender
            most = total
    return best


# ---- bench harness ---------------------------------------------------------

seed = 2284


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(length):
    return "".join(chr(ord("a") + next_random() % 26) for _ in range(length))


def main():
    pool = []
    for _ in range(40):
        length = next_random() % 10 + 1
        pool.append(word(length))
    cases = []
    for _ in range(1000):
        first = next_random() % 20
        messages = []
        senders = []
        for _ in range(100):
            senders.append(pool[first + next_random() % 20])
            w = next_random() % 8 + 1
            parts = []
            for _ in range(w):
                length = next_random() % 5 + 1
                parts.append(word(length))
            messages.append(" ".join(parts))
        cases.append((messages, senders))
    check = 0
    for _ in range(20):
        for messages, senders in cases:
            best = largest_word_count(messages, senders)
            check = (check * 31 + sum(best.encode())) % 1000000007
    print(f"20 passes over 1000 cases of 100 messages: checksum {check}")


main()
