# LeetCode #2350: Shortest Impossible Sequence of Rolls -- the bench, the ★
# arm in Python: the rolls cut greedily into pieces that each hold every
# face, with a table of the faces seen in the current piece made afresh at
# its end.


def shortest_sequence(rolls, k):
    seen = [False] * (k + 1)
    distinct = 0
    pieces = 0
    for r in rolls:
        if not seen[r]:
            seen[r] = True
            distinct += 1
            if distinct == k:
                pieces += 1
                distinct = 0
                seen = [False] * (k + 1)
    return pieces + 1


SEED = [2350]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # 10 arrays of 10^5 rolls, of dice with 2 to 10^4 faces
    faces = [2, 3, 6, 10, 20, 50, 100, 1000, 3000, 10000]
    arrays = []
    for a in range(10):
        k = faces[a]
        rolls = []
        for _ in range(100000):
            high = next_random()
            rolls.append((high * 32768 + next_random()) % k + 1)
        arrays.append(rolls)
    check = 0
    for p in range(50):
        for a in range(10):
            check = (check * 31 + shortest_sequence(arrays[a], faces[a]) + p) % 1000000007
    print(f"50 passes over 10 arrays of 10^5 rolls: checksum {check}")


main()
