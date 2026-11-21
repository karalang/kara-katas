# LeetCode #1652: Defuse the Bomb -- the bench's Python mirror: the ★ arm
# on 400 random codes of 100000 numbers from 1 to 100, each with a k from
# -99999 to 99999, all drawn first.


def decrypt(code, k):
    n = len(code)
    answer = [0] * n
    if k == 0:
        return answer
    start, end = (1, k) if k > 0 else (n + k, n - 1)
    s = 0
    for j in range(start, end + 1):
        s += code[j % n]
    for i in range(n):
        answer[i] = s
        s -= code[start % n]
        start += 1
        end += 1
        s += code[end % n]
    return answer


seed = 1652


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


n = 100000
codes = []
for _ in range(400):
    code = [next_random() % 100 + 1 for _ in range(n)]
    k = (next_random() * 32768 + next_random()) % (2 * n - 1) - (n - 1)
    codes.append((code, k))
check = 0
total = 0
for code, k in codes:
    for x in decrypt(code, k):
        total += x
        check = (check * 31 + x + 1) % 1000000007
print(f"400 codes of 100000 numbers: answers sum to {total}, checksum {check}")
