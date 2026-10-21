# Python mirror of the ★ arm plus harness for kata 837.

def new21_game(n, k, max_pts):
    if k == 0 or n >= k - 1 + max_pts:
        return 1.0
    w = float(max_pts)
    p = [0.0] * (n + 1)
    p[0] = 1.0
    window = 1.0
    answer = 0.0
    for i in range(1, n + 1):
        p[i] = window / w
        if i < k:
            window += p[i]
        else:
            answer += p[i]
        gone = i - max_pts
        if gone >= 0 and gone < k:
            window -= p[gone]
    return answer

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def show(n, k, max_pts):
    print(f"n = {n}, k = {k}, maxPts = {max_pts}: {new21_game(n, k, max_pts):.6f}")

def main():
    global seed
    show(10, 1, 10)
    show(6, 1, 10)
    show(21, 17, 10)
    show(0, 0, 1)
    show(1, 1, 2)
    show(5, 3, 1)
    show(3, 3, 2)
    show(4, 3, 3)
    show(10000, 10000, 10000)
    show(10000, 5000, 10000)
    show(10000, 9999, 2)
    show(10000, 10000, 1)
    show(5000, 4999, 10000)
    seed = 837
    s = 0.0
    above = 0
    for _ in range(300):
        n = next_random() % 10001
        k = next_random() % (n + 1)
        max_pts = 1 + next_random() % 10000
        x = new21_game(n, k, max_pts)
        s += x
        if x > 0.5:
            above += 1
    print(f"300 random games: sum {s:.6f}, {above} above one half")

main()
