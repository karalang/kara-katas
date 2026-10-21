# Python mirror of the ★ arm plus harness for kata 838.

def push_dominoes(dominoes):
    d = list(dominoes)
    n = len(d)
    left = -1
    left_push = 'L'
    for right in range(n + 1):
        right_push = 'R' if right == n else d[right]
        if right_push == '.':
            continue
        if left_push == right_push:
            for i in range(left + 1, right):
                d[i] = right_push
        elif left_push == 'R':
            i = left + 1
            j = right - 1
            while i < j:
                d[i] = 'R'
                d[j] = 'L'
                i += 1
                j -= 1
        left = right
        left_push = right_push
    return ''.join(d)

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_line(n, pushed):
    s = []
    for _ in range(n):
        r = next_random() % 200
        s.append('L' if r < pushed else 'R' if r < 2 * pushed else '.')
    return ''.join(s)

def fold(check, s):
    c = check
    for b in s.encode():
        c = (c * 31 + b) % 1000000007
    return c

def show(dominoes):
    print(f'"{dominoes}" -> "{push_dominoes(dominoes)}"')

def main():
    global seed
    for s in ["RR.L", ".L.R...LR..L..", ".", "R", "L", "R.L", "R..L", "R...", "...L", "L...R", "R.R.L", ".L.R.", "R....L.....L"]:
        show(s)
    seed = 838
    for pushed in [1, 10, 60]:
        out = push_dominoes(random_line(100000, pushed))
        print(f"100000 dominoes, {pushed} in 200 pushed each way: {out.count('L')} L, {out.count('R')} R, {out.count('.')} up, checksum {fold(0, out)}")
    check = 0
    up = 0
    for _ in range(300):
        n = 1 + next_random() % 60
        pushed = next_random() % 51
        out = push_dominoes(random_line(n, pushed))
        up += out.count('.')
        check = fold(check, out)
    print(f"300 random lines: {up} left standing, checksum {check}")

main()
