# LeetCode #1053: Previous Permutation With One Swap -- Python mirror of
# bench/prev_perm.kara.


def prev_perm_opt1(arr):
    out = list(arr)
    n = len(out)
    i = n - 2
    while i >= 0 and out[i] <= out[i + 1]:
        i -= 1
    if i < 0:
        return out
    j = n - 1
    while out[j] >= out[i]:
        j -= 1
    while out[j - 1] == out[j]:
        j -= 1
    out[i], out[j] = out[j], out[i]
    return out


seed = 1053


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 200, 20000, 25
    all_ = []
    for _ in range(count):
        run = next_random() % (n - 1) + 1
        arr = [next_random() % 10000 + 1 for _ in range(n - run)]
        v = next_random() % 1000 + 1
        for _ in range(run):
            arr.append(v)
            v += next_random() % 3
        all_.append((arr, n - run - 1))
    total = 0
    check = 0
    for _ in range(rounds):
        for arr, start in all_:
            answer = prev_perm_opt1(arr)
            h = 0
            for k in range(start, n):
                h = (h * 10007 + answer[k]) % 1000000007
            total += answer[start]
            check = (check * 131 + h) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: total {total}, checksum {check}")


main()
