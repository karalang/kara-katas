# LeetCode #1023: Camelcase Matching -- bench
# Mirrors ./camel_match.kara; see ../README.md § Benchmarks.


def camel_match(queries, pattern):
    p = list(pattern)
    answers = []
    for query in queries:
        i = 0
        ok = True
        for c in query:
            if i < len(p) and c == p[i]:
                i += 1
            elif "A" <= c <= "Z":
                ok = False
                break
        answers.append(ok and i == len(p))
    return answers


def main():
    count = 500
    rounds = 150
    seed = 1023

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random_letter(capitals):
        upper = next_random() % 8 < capitals
        k = next_random() % 26
        return chr((65 if upper else 97) + k)

    cases = []
    letters = 0
    for _ in range(count):
        plen = 1 + next_random() % 100
        pattern = "".join(random_letter(2) for _ in range(plen))
        queries = []
        for k in range(100):
            q = []
            if k % 2 == 0:
                left = next_random() % (100 - plen + 1)
                at = 0
                while at < plen or left > 0:
                    if left > 0 and (at == plen or next_random() % 2 == 0):
                        q.append(random_letter(1))
                        left -= 1
                    else:
                        q.append(pattern[at])
                        at += 1
            else:
                for _ in range(1 + next_random() % 100):
                    q.append(random_letter(2))
            q = "".join(q)
            letters += len(q)
            queries.append(q)
        cases.append((pattern, queries))
    matched = 0
    check = 0
    for _ in range(rounds):
        for pattern, queries in cases:
            for k, answer in enumerate(camel_match(queries, pattern)):
                if answer:
                    matched += 1
                    check = (check * 31 + k + 1) % 1000000007
    print(f"{count} cases, {letters} query letters, {rounds} rounds: {matched} match, checksum {check}")


main()
