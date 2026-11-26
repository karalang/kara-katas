# LeetCode #1769: Minimum Number of Operations to Move All Balls to Each
# Box -- the bench in Python, mirroring min_operations.kara: two sweeps,
# the moves for the balls on each side growing by the balls seen so far.

def min_operations(boxes):
    n = len(boxes)
    answer = [0] * n
    balls = moves = 0
    for i in range(n):
        answer[i] += moves
        if boxes[i] == "1":
            balls += 1
        moves += balls
    balls = moves = 0
    for i in range(n - 1, -1, -1):
        answer[i] += moves
        if boxes[i] == "1":
            balls += 1
        moves += balls
    return answer

seed = 1769
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def main():
    rows = []
    for _ in range(200):
        full = next_random() % 101
        rows.append("".join("1" if next_random() % 100 < full else "0" for _ in range(2000)))
    check = 0
    for call in range(40000):
        answer = min_operations(rows[(check + call * 7919) % 200])
        check = (check * 31 + answer[check % 2000]) % 1000000007
    print(f"40000 calls over 200 rows: checksum {check}")

main()
