# LeetCode #1700: Number of Students Unable to Eat Lunch -- the bench's
# Python mirror: the ★ arm on 50000 random lunches of 100 students, all
# drawn first, each answered 80 times.


def count_students(students, sandwiches):
    wanting = [0, 0]
    for s in students:
        wanting[s] += 1
    for s in sandwiches:
        if wanting[s] == 0:
            break
        wanting[s] -= 1
    return wanting[0] + wanting[1]


seed = 1700


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 50000, 80, 100
    lunches = []
    for _ in range(count):
        lean = next_random() % 11
        students = [1 if next_random() % 10 < lean else 0 for _ in range(n)]
        sandwiches = [1 if next_random() % 10 < lean else 0 for _ in range(n)]
        lunches.append((students, sandwiches))
    total = 0
    check = 0
    for r in range(rounds):
        for students, sandwiches in lunches:
            answer = count_students(students, sandwiches)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} lunches of {n} students, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
