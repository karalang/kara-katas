# Benchmark for #552: Python mirror of the ★ arm (six counters, rolled);
# see student_attendance_record_ii.kara.

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


def main():
    checksum = days = 0
    for k in range(100):
        n = 100000 - (k * 997) % 1000
        days += n
        checksum = (checksum * 31 + check_record(n)) % 1000000007
    print(f"100 lengths, {days} days: checksum {checksum}")


main()
