# LeetCode #2284: Sender With Largest Word Count -- the Python mirror of
# the ★ arm, `words.kara`.


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


# ---- test harness ---------------------------------------------------------

seed = 2284


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        (
            ["Hello userTwooo", "Hi userThree", "Wonderful day Alice", "Nice day userThree"],
            ["Alice", "userTwo", "userThree", "Alice"],
        ),
        (["How is leetcode for everyone", "Leetcode is useful for practice"], ["Bob", "Charlie"]),
        (["a b", "c d"], ["bob", "Bob"]),
        (["x y z", "x y", "q"], ["Alice", "Al", "Al"]),
        (["one"], ["Z"]),
    ]
    for messages, senders in cases:
        print(f"[{', '.join(senders)}] -> {largest_word_count(messages, senders)}")
    pool = ["Al", "al", "Alice", "alice", "B", "b", "Bo", "Zed", "zed", "ZED"]
    check = 0
    first = 0
    for _ in range(3000):
        n = next_random() % 40 + 1
        k = next_random() % 7 + 2
        messages = []
        senders = []
        for _ in range(n):
            senders.append(pool[next_random() % k])
            w = next_random() % 6 + 1
            message = ""
            for j in range(w):
                if j > 0:
                    message += " "
                length = next_random() % 3 + 1
                for _ in range(length):
                    message += chr(ord("a") + next_random() % 26)
            messages.append(message)
        answer = largest_word_count(messages, senders)
        at = 0
        for i, name in enumerate(pool):
            if name == answer:
                at = i + 1
        check = (check * 31 + at) % 1000000007
        if at == 1:
            first += 1
    print(f"3000 cases: checksum {check}, {first} won by Al")


main()
