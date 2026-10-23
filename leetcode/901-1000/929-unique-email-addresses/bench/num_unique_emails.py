# LeetCode #929: Unique Email Addresses -- bench: one walk per address and
# a set. Mirrors num_unique_emails.kara.


def num_unique_emails(emails):
    seen = set()
    for e in emails:
        out = []
        domain = False
        tagged = False
        for c in e:
            if domain:
                out.append(c)
            elif c == "@":
                domain = True
                out.append(c)
            elif c == "+":
                tagged = True
            elif c != "." and not tagged:
                out.append(c)
        seen.add("".join(out))
    return len(seen)


seed = 929


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count = 300, 100
    domains = ["@leetcode.com", "@lee.tcode.com", "@example.com", "@mail.example.com", "@a+b.com", "@ab.com", "@kara.dev.com", "@x.com"]
    # count lists of 100 addresses, built once: a local name of 2 to 7
    # letters from "ab" with a dot before about one in four, a tag after a
    # '+' on half of them, and one of eight domains
    lists = []
    for _ in range(count):
        emails = []
        for _ in range(100):
            b = []
            letters = 2 + next_random() % 6
            for _ in range(letters):
                if next_random() % 4 == 0:
                    b.append(".")
                b.append(chr(ord("a") + next_random() % 2))
            if next_random() % 2 == 0:
                b.append("+")
                for _ in range(next_random() % 10):
                    b.append(chr(ord("a") + next_random() % 26))
            emails.append("".join(b) + domains[next_random() % 8])
        lists.append(emails)
    total = 0
    check = 0
    for r in range(rounds):
        # each round visits every list, starting from a different one
        for i in range(count):
            a = num_unique_emails(lists[(r + i) % count])
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over {count} lists of 100 addresses: answers summing to {total}, checksum {check}")


main()
