# LeetCode #1769: Minimum Number of Operations to Move All Balls to Each
# Box -- the ★ arm in Python: two sweeps, the moves for the balls on each
# side growing by the balls seen so far.

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

seed = 0
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_boxes(n, full):
    return "".join("1" if next_random() % 100 < full else "0" for _ in range(n))

def digest(answer):
    check = len(answer)
    for a in answer:
        check = (check * 31 + a) % 1000000007
    return check

def show(v):
    return "[" + ", ".join(map(str, v)) + "]"

def main():
    global seed
    print(show(min_operations("110")), show(min_operations("001011")))
    print(" ".join(show(min_operations(s)) for s in ["0", "1", "0000", "1111", "100001"]))
    seed = 1769
    full = "1" * 2000
    half = random_boxes(2000, 50)
    a = min_operations(full)
    b = min_operations(half)
    print(f"the most: {a[0]} {a[1999]} {digest(a)}, {digest(b)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 40
        f = next_random() % 101
        boxes = random_boxes(n, f)
        check = (check * 31 + digest(min_operations(boxes))) % 1000000007
    print(f"3000 random rows: checksum {check}")

main()
