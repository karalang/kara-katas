# LeetCode #551: Student Attendance Record I -- Python mirror of the ★
# arm (one pass, two counters); see student_attendance_record_i.kara.


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


# ---- test harness ---------------------------------------------------------

seed = 551


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_record(n, a, l):
    out = []
    for _ in range(n):
        r = next_random() % 100
        out.append("A" if r < a else "L" if r < a + l else "P")
    return "".join(out)


def word(b):
    return "true" if b else "false"


def show(s):
    print(f'"{s}" -> {word(check_record(s))}')


def main():
    for s in ["PPALLP", "PPALLL", "P", "A", "AA", "LL", "LLL", "LLPLLPLLA", "ALLPLLLA", "PLLAPLL", "APA"]:
        show(s)
    days = fine = h = 0
    for t in range(300):
        n = 1 + next_random() % 20
        a = 3 if t % 3 == 0 else 10 if t % 3 == 1 else 20
        l = 30 if t % 3 == 0 else 50 if t % 3 == 1 else 70
        bit = 1 if check_record(random_record(n, a, l)) else 0
        days += n
        fine += bit
        h = (h * 31 + bit + 7 * n) % 1000000007
    print(f"300 random records: {days} days, {fine} fine, checksum {h}")
    print(f"1000 days present: {word(check_record('P' * 1000))}")
    print(f"333 pairs of lates and one absence: {word(check_record('LLP' * 333 + 'A'))}")
    print(f"three lates on the last days: {word(check_record('P' * 997 + 'LLL'))}")
    print(f"absent on the first and last days: {word(check_record('A' + 'P' * 998 + 'A'))}")


main()
