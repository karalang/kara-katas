# Benchmark for #551: Python mirror of the ★ arm (one pass, two
# counters); see student_attendance_record_i.kara.


def check_record(s):
    absences = 0
    lates = 0
    for c in s:
        if c == "L":
            lates += 1
            if lates == 3:
                return False
        else:
            lates = 0
            if c == "A":
                absences += 1
                if absences == 2:
                    return False
    return True


seed = 551


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 1000
    records = []
    for _ in range(count):
        out = []
        for _ in range(1000):
            r = next_random() % 2000
            out.append("A" if r < 1 else "L" if r < 101 else "P")
        records.append("".join(out))
    fine = checksum = 0
    for rnd in range(300):
        for g in range(count):
            bit = 1 if check_record(records[(rnd * 7 + g) % count]) else 0
            fine += bit
            checksum = (checksum * 31 + bit + g) % 1000000007
    print(f"{count} records, 300 rounds each: {fine} fine, checksum {checksum}")


main()
