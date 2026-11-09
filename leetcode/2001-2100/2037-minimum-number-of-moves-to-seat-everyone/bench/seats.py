# LeetCode #2037: Minimum Number of Moves to Seat Everyone -- the ★ arm in
# Python, the same algorithm and workload as seats.kara: both lists copied
# and sorted, the k-th seat paired with the k-th student, the distances
# summed.


def min_moves_to_seat(seats, students):
    seats = sorted(seats)
    students = sorted(students)
    return sum(abs(a - b) for a, b in zip(seats, students))


seed = 2037


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    seats = []
    students = []
    for _ in range(2000):
        seats.append([next_random() % 100 + 1 for _ in range(100)])
        students.append([next_random() % 100 + 1 for _ in range(100)])
    calls = 0
    total = 0
    check = 0
    for rnd in range(25):
        for r in range(2000):
            at = (rnd * 37 + r * 11) % 100
            seats[r][at] = seats[r][at] % 100 + 1
            answer = min_moves_to_seat(seats[r], students[r])
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
