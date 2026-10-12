# LeetCode #406: Queue Reconstruction by Height -- mirror of
# queue_reconstruction.kara (tallest first, each inserted at its k).


def reconstruct_queue(people):
    order = sorted(people, key=lambda p: (-p[0], p[1]))
    queue = []
    for p in order:
        queue.insert(p[1], p)
    return queue


seed = 406


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def text(people):
    return "[" + ", ".join(f"[{h}, {k}]" for h, k in people) + "]"


def show(people):
    print(f"{text(people)} -> {text(reconstruct_queue(people))}")


show([(7, 0), (4, 4), (7, 1), (5, 0), (6, 1), (5, 2)])
show([(6, 0), (5, 0), (4, 0), (3, 2), (2, 2), (1, 4)])
show([])
show([(5, 0)])
show([(3, 2), (3, 0), (3, 1)])
show([(3, 0), (2, 0), (1, 0)])
show([(1, 2), (3, 0), (2, 1)])
show([(2, 0), (1, 1), (2, 1), (1, 0)])
rebuilt = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 50
    line = []
    for i in range(n):
        h = 1 + step() % 20
        k = sum(1 for (g, _) in line if g >= h)
        line.append((h, k))
    shuffled = list(line)
    for i in range(n - 1, 0, -1):
        j = step() % (i + 1)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    q = reconstruct_queue(shuffled)
    if q == line:
        rebuilt += 1
    for h, k in q:
        checksum = (checksum * 31 + h * 100 + k) % 1000000007
print(f"2000 random queues: {rebuilt} rebuilt, checksum {checksum}")
