# Benchmark for #858: Mirror Reflection -- Python twin of the trace arm (the
# ray traced from wall to wall), in every room LeetCode allows.


def mirror_reflection(p, q):
    y = 0
    up = True
    east = False
    while True:
        if up:
            y += q
            if y > p:
                y = 2 * p - y
                up = False
        else:
            y -= q
            if y < 0:
                y = -y
                up = True
        east = not east
        if y == p:
            return 1 if east else 2
        # the south-west corner is never reached, so this is the east wall
        if y == 0:
            return 0


def main():
    counts = [0, 0, 0]
    check = 0
    for p in range(1, 1001):
        for q in range(1, p + 1):
            r = mirror_reflection(p, q)
            counts[r] += 1
            check = (check * 3 + r) % 1000000007
    print(f"500500 rooms: receptor 0 {counts[0]} times, 1 {counts[1]}, 2 {counts[2]}, checksum {check}")


main()
