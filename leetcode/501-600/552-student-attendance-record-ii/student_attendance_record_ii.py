# LeetCode #552: Student Attendance Record II -- Python mirror of the ★
# arm (six counters, rolled); see student_attendance_record_ii.kara.

M = 1000000007


def check_record(n):
    count = [1, 0, 0, 0, 0, 0]
    for _ in range(n):
        nxt = [0] * 6
        for a in range(2):
            for l in range(3):
                c = count[a * 3 + l]
                if c == 0:
                    continue
                nxt[a * 3] = (nxt[a * 3] + c) % M
                if a == 0:
                    nxt[3] = (nxt[3] + c) % M
                if l < 2:
                    nxt[a * 3 + l + 1] = (nxt[a * 3 + l + 1] + c) % M
        count = nxt
    total = 0
    for c in count:
        total = (total + c) % M
    return total


# ---- test harness ---------------------------------------------------------

seed = 552


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"example 1: n = 2 -> {check_record(2)}")
    print(f"example 2: n = 1 -> {check_record(1)}")
    print(f"example 3: n = 10101 -> {check_record(10101)}")
    small = [check_record(n) for n in range(1, 13)]
    print(f"n = 1 to 12: [{', '.join(str(x) for x in small)}]")
    days = h = 0
    for _ in range(300):
        n = 1 + next_random() % 2000
        days += n
        h = (h * 31 + check_record(n)) % 1000000007
    print(f"300 random lengths: {days} days, checksum {h}")
    for n in [1000, 9999, 50000, 99999, 100000]:
        print(f"n = {n} -> {check_record(n)}")


main()
