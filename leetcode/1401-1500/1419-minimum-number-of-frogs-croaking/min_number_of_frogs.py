# LeetCode #1419, Python mirror of min_number_of_frogs.kara: how many times
# each letter has been heard, no letter more often than the one before it
# in `croak`, the frogs croaking at once those that said `c` and not yet
# `k`, and every croak finished at the end.


def min_number_of_frogs(croak_of_frogs):
    heard = [0, 0, 0, 0, 0]
    most = 0
    for c in croak_of_frogs:
        i = "croak".find(c)
        if i < 0:
            return -1
        heard[i] += 1
        if i > 0 and heard[i] > heard[i - 1]:
            return -1
        most = max(most, heard[0] - heard[4])
    return most if heard[0] == heard[4] else -1


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def heard(m, spread):
    word = "croak"
    s = []
    croaking = []
    started = 0
    while started < m or croaking:
        r = next_random()
        if started < m and (not croaking or r % spread == 0):
            s.append("c")
            croaking.append(1)
            started += 1
        else:
            i = r // spread % len(croaking)
            s.append(word[croaking[i]])
            croaking[i] += 1
            if croaking[i] == 5:
                croaking[i] = croaking[-1]
                croaking.pop()
    return "".join(s)


def spoiled(s):
    chars = list(s)
    r = next_random()
    at = r // 3 % len(chars)
    if r % 3 == 0:
        chars[at] = "croak"[next_random() % 5]
    elif r % 3 == 1:
        del chars[at]
    elif at + 1 < len(chars):
        chars[at], chars[at + 1] = chars[at + 1], chars[at]
    return "".join(chars)


def main():
    global seed
    cases = ["croakcroak", "crcoakroak", "croakcrook", "c", "croak", "kcroa", "ccrrooaakk", "crocakcroraoakk"]
    print(" ".join(str(min_number_of_frogs(s)) for s in cases))
    seed = 1419
    together = "".join(l * 20000 for l in "croak")
    after = "croak" * 20000
    drawn = heard(20000, 2)
    print(f"10^5 letters: {min_number_of_frogs(together)} {min_number_of_frogs(after)} {min_number_of_frogs(drawn)}")
    check = 0
    invalid = 0
    for i in range(2000):
        m = 1 + next_random() % 40
        spread = 1 + next_random() % 6
        s = heard(m, spread)
        if i % 3 == 0:
            s = spoiled(s)
        got = min_number_of_frogs(s)
        if got < 0:
            invalid += 1
        check = (check * 131 + got + 1) % 1000000007
    print(f"2000 random cases: {invalid} invalid, checksum {check}")


main()
