# LeetCode #1023: Camelcase Matching -- two pointers
# Mirrors camel_match.kara (the ★ arm) and prints the same output.


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


seed = 1023


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_letter(letters, capitals):
    upper = next_random() % 8 < capitals
    k = next_random() % letters
    return chr((65 if upper else 97) + k)


def grown(pattern, extra, letters, stray):
    out = []
    k = 0
    left = extra
    while k < len(pattern) or left > 0:
        if left > 0 and (k == len(pattern) or next_random() % 2 == 0):
            out.append(random_letter(letters, stray))
            left -= 1
        else:
            out.append(pattern[k])
            k += 1
    return "".join(out)


def show(answers):
    return "[" + ", ".join("true" if a else "false" for a in answers) + "]"


def main():
    queries = ["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"]
    for pattern in ["FB", "FoBa", "FoBaT"]:
        print(f"{pattern}: {show(camel_match(queries, pattern))}")
    small = ["a", "A", "ba", "ab", "Ba", "aB", "aa", "b"]
    for pattern in ["a", "A", "aa", "B"]:
        print(f"{pattern}: {show(camel_match(small, pattern))}")
    groups = [(2000, 4, 3, 2, 3), (1000, 10, 8, 3, 2), (300, 30, 20, 4, 2), (100, 100, 40, 5, 1), (30, 100, 100, 26, 1), (100, 100, 2, 26, 4)]
    for cases, count, length, letters, capitals in groups:
        matched = 0
        check = 0
        for _ in range(cases):
            plen = 1 + next_random() % length
            pattern = "".join(random_letter(letters, capitals) for _ in range(plen))
            qs = []
            for k in range(count):
                room = 100 - plen
                extra = 0 if room == 0 else next_random() % (min(room, length) + 1)
                if k % 2 == 0:
                    qs.append(grown(pattern, extra, letters, 1))
                else:
                    n = 1 + next_random() % max(length, plen)
                    qs.append("".join(random_letter(letters, capitals) for _ in range(n)))
            for answer in camel_match(qs, pattern):
                if answer:
                    matched += 1
                check = (check * 3 + (2 if answer else 1)) % 1000000007
        print(f"{cases} cases of {count} queries ({letters} letters, {capitals}/8 capitals): {matched} match, checksum {check}")


main()
