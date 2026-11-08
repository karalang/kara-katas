# LeetCode #2007: Find Original Array From Doubled Array -- the mirror of the
# ★ arm, doubled.kara; its output is byte-identical.


def find_original_array(changed):
    if len(changed) % 2 == 1:
        return []
    top = max(changed)
    count = [0] * (top + 1)
    for x in changed:
        count[x] += 1
    if count[0] % 2 == 1:
        return []
    original = [0] * (count[0] // 2)
    for v in range(1, top + 1):
        c = count[v]
        if c == 0:
            continue
        if 2 * v > top or count[2 * v] < c:
            return []
        count[2 * v] -= c
        original.extend([v] * c)
    return original


seed = 2007


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


# any order of the original is an answer, so the answer is shown sorted
def sorted_answer(changed):
    return sorted(find_original_array(changed))


# a doubled array of `n` values up to `top`, shuffled, then with probability
# one in three one value nudged, which usually spoils it
def random_changed(n, top):
    changed = []
    for _ in range(n):
        x = next_random() % (top + 1)
        changed.append(x)
        changed.append(2 * x)
    for i in range(len(changed) - 1, 0, -1):
        j = next_random() % (i + 1)
        changed[i], changed[j] = changed[j], changed[i]
    if next_random() % 3 == 0:
        i = next_random() % len(changed)
        changed[i] += 1
    return changed


def fold(answer, acc):
    acc[0] += len(answer)
    acc[1] = mix(acc[1], len(answer))
    for a in answer:
        acc[0] += a
        acc[1] = mix(acc[1], a)


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's three examples, then a few more
    examples = [
        [1, 3, 4, 2, 6, 8],
        [6, 3, 0, 1],
        [1],
        [0, 0, 0, 0],
        [0, 0, 0],
        [4, 2, 2, 1, 8, 4],
        [2, 1, 2, 4, 2, 4],
        [3, 6, 6, 12],
    ]
    for changed in examples:
        print(f"{show(changed)} -> {show(sorted_answer(changed))}")
    acc = [0, 0]
    for _ in range(3000):
        n = next_random() % 8 + 1
        top = next_random() % 12
        fold(sorted_answer(random_changed(n, top)), acc)
    print(f"3000 arrays of 2 to 16 values: sum {acc[0]}, checksum {acc[1]}")
    acc = [0, 0]
    for a in range(6):
        top = [3, 100, 50000][a % 3]
        fold(sorted_answer(random_changed(20000, top)), acc)
    print(f"6 arrays of 40000 values: sum {acc[0]}, checksum {acc[1]}")


main()
