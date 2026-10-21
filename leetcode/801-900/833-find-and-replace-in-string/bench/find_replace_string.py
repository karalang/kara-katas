# Benchmark for #833: Find And Replace in String -- the ★ arm (a table by index).
#
# Mirrors find_replace_string.kara: each operation whose source occurs at
# its index is recorded in a table at that index, and one walk over the
# string writes each recorded operation's target in place of its source
# and copies the other letters.

import sys


def find_replace_string(s, indices, sources, targets):
    n = len(s)
    at = [-1] * n
    for k in range(len(indices)):
        i = indices[k]
        if s.startswith(sources[k], i):
            at[i] = k
    out = []
    i = 0
    while i < n:
        k = at[i]
        if k >= 0:
            out.append(targets[k])
            i += len(sources[k])
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


seed = 833


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(r):
    return chr(97 + r)


def main():
    count = 64
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
    n = 1000
    cases = []
    for _ in range(count):
        s = "".join(letter(next_random() % 2) for _ in range(n))
        indices, sources, targets = [], [], []
        pos = next_random() % 4
        while pos < n and len(indices) < 100:
            room = n - pos if n - pos < 10 else 10
            length = 1 + next_random() % room
            src = s[pos:pos + length]
            if next_random() % 3 == 2:
                last = ord(src[length - 1]) - 97
                src = src[:length - 1] + letter((last + 1) % 26)
            tlen = 1 + next_random() % 7
            target = "".join(letter(next_random() % 26) for _ in range(tlen))
            indices.append(pos)
            sources.append(src)
            targets.append(target)
            pos += length + next_random() % 4
        i = len(indices)
        while i > 1:
            j = next_random() % i
            i -= 1
            indices[i], indices[j] = indices[j], indices[i]
            sources[i], sources[j] = sources[j], sources[i]
            targets[i], targets[j] = targets[j], targets[i]
        cases.append((s, indices, sources, targets))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        s, indices, sources, targets = cases[rnd % count]
        out = find_replace_string(s, indices, sources, targets)
        total += len(out)
        checksum = (checksum * 131 + ord(out[rnd // count % len(out)])) % 1000000007
    print(f"{rounds} rounds of {count} cases: {total} letters, checksum {checksum}")


main()
