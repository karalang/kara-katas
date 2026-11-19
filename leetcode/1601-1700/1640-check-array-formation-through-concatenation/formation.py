# LeetCode #1640: Check Array Formation Through Concatenation -- the Python
# mirror of the ★ arm: a dict from each piece's first value to the piece,
# and one walk of the array.


def can_form_array(arr, pieces):
    starting = {piece[0]: k for k, piece in enumerate(pieces)}
    i = 0
    while i < len(arr):
        if arr[i] not in starting:
            return False
        for value in pieces[starting[arr[i]]]:
            if i >= len(arr) or arr[i] != value:
                return False
            i += 1
    return True


# ---- the harness: the same as every arm's ---------------------------------

seed = 1640


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distinct(n, top):
    chosen = set()
    values = []
    while len(values) < n:
        v = next_random() % top + 1
        if v not in chosen:
            chosen.add(v)
            values.append(v)
    return values


def batch(count, most):
    check = 0
    trues = 0
    for _ in range(count):
        n = next_random() % most + 1
        arr = distinct(n, 2 * most)
        pieces = []
        start = 0
        while start < n:
            end = min(n, start + next_random() % 3 + 1)
            pieces.append(arr[start:end])
            start = end
        for k in range(len(pieces) - 1, 0, -1):
            j = next_random() % (k + 1)
            pieces[k], pieces[j] = pieces[j], pieces[k]
        change = next_random() % 3
        if change == 1 and n > 1:
            a, b = next_random() % n, next_random() % n
            arr[a], arr[b] = arr[b], arr[a]
        elif change == 2:
            k = next_random() % n
            arr[k] = 2 * most + 1
        formed = can_form_array(arr, pieces)
        if formed:
            trues += 1
        check = (check * 31 + (2 if formed else 1)) % 1000000007
    print(f"{count} cases of up to {most} values: {trues} can be formed, checksum {check}")


def show(b):
    print("true" if b else "false")


show(can_form_array([15, 88], [[88], [15]]))
show(can_form_array([49, 18, 16], [[16, 18, 49]]))
show(can_form_array([91, 4, 64, 78], [[78], [4, 64], [91]]))
show(can_form_array([1], [[1]]))
show(can_form_array([1, 2, 3], [[1], [3, 2]]))
batch(3000, 6)
batch(300, 100)
batch(20, 5000)
