# LeetCode #1700: Number of Students Unable to Eat Lunch -- mirrors
# lunch.kara, the ★ arm: only how many want each kind matters.


def count_students(students, sandwiches):
    wanting = [0, 0]
    for s in students:
        wanting[s] += 1
    for s in sandwiches:
        if wanting[s] == 0:
            break
        wanting[s] -= 1
    return wanting[0] + wanting[1]


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = seed.next() % most + 1
        lean = seed.next() % 11
        students = [1 if seed.next() % 10 < lean else 0 for _ in range(n)]
        sandwiches = [1 if seed.next() % 10 < lean else 0 for _ in range(n)]
        answer = count_students(students, sandwiches)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} lunches of up to {most} students: answers sum to {total}, checksum {check}")


def main():
    print(count_students([1, 1, 0, 0], [0, 1, 0, 1]))
    print(count_students([1, 1, 1, 0, 0, 1], [1, 0, 0, 0, 1, 1]))
    print(count_students([0], [1]))
    print(count_students([1], [1]))
    seed = Seed(1700)
    batch(3000, 12, seed)
    batch(300, 100, seed)
    batch(10, 10000, seed)


main()
