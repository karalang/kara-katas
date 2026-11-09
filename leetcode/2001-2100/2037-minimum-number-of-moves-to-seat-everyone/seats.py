# LeetCode #2037: Minimum Number of Moves to Seat Everyone -- the ★ arm in
# Python, the same algorithm and harness as seats.kara: both lists sorted,
# the k-th seat paired with the k-th student, the distances summed.


def min_moves_to_seat(seats, students):
    seats = sorted(seats)
    students = sorted(students)
    return sum(abs(a - b) for a, b in zip(seats, students))


seed = 2037


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def random_positions(n, top):
    return [next_random() % top + 1 for _ in range(n)]


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([3, 1, 5], [2, 7, 4]),
        ([4, 1, 5, 9], [1, 3, 2, 6]),
        ([2, 2, 6, 6], [1, 3, 2, 6]),
        ([1], [100]),
        ([7, 7, 7], [7, 7, 7]),
        ([1, 100], [100, 1]),
        ([5, 3, 9, 1, 1], [2, 2, 8, 10, 4]),
    ]
    for seats, students in examples:
        print(f"{show(seats)} {show(students)} -> {min_moves_to_seat(seats, students)}")
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 100 + 1
        top = next_random() % 100 + 1
        seats = random_positions(n, top)
        students = random_positions(n, top)
        answer = min_moves_to_seat(seats, students)
        total += answer
        check = mix(check, answer)
    print(f"2000 rooms of up to 100 seats: sum {total}, checksum {check}")


main()
