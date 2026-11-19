# LeetCode #1640: Check Array Formation Through Concatenation -- the
# bench's Python mirror: the ★ arm on 50000 random cases of the values 1 to
# 100 in a random order, cut into pieces of 1 to 3 and shuffled, every
# third one with two values swapped, all drawn first.


def can_form_array(arr, pieces):
    starting = {}
    for k, piece in enumerate(pieces):
        starting[piece[0]] = k
    i = 0
    while i < len(arr):
        k = starting.get(arr[i])
        if k is None:
            return False
        for value in pieces[k]:
            if i >= len(arr) or arr[i] != value:
                return False
            i += 1
    return True


seed = 1640


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for c in range(50000):
        arr = list(range(1, 101))
        for k in range(99, 0, -1):
            j = next_random() % (k + 1)
            arr[k], arr[j] = arr[j], arr[k]
        pieces = []
        start = 0
        while start < 100:
            end = min(100, start + next_random() % 3 + 1)
            pieces.append(arr[start:end])
            start = end
        for k in range(len(pieces) - 1, 0, -1):
            j = next_random() % (k + 1)
            pieces[k], pieces[j] = pieces[j], pieces[k]
        if c % 3 == 2:
            a, b = next_random() % 100, next_random() % 100
            arr[a], arr[b] = arr[b], arr[a]
        cases.append((arr, pieces))
    check = 0
    trues = 0
    for arr, pieces in cases:
        formed = can_form_array(arr, pieces)
        if formed:
            trues += 1
        check = (check * 31 + (2 if formed else 1)) % 1000000007
    print(f"50000 cases of 100 values: {trues} can be formed, checksum {check}")


main()
