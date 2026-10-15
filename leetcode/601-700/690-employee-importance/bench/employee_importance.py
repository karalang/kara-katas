# LeetCode #690: Employee Importance -- breadth first, by id. Bench.
#
# 30 companies of 2,000 people, ids 1 to 2000 in random order, each
# person under a random earlier one, are built once, with 100 random
# people to ask about in each; then 80 rounds ask about all of them.
from collections import deque


class Employee:
    def __init__(self, id, importance, subordinates):
        self.id = id
        self.importance = importance
        self.subordinates = subordinates


def get_importance(employees, id):
    at = [-1] * 2001
    for i in range(len(employees)):
        at[employees[i].id] = i
    queue = deque([id])
    total = 0
    while queue:
        e = employees[at[queue.popleft()]]
        total += e.importance
        for s in e.subordinates:
            queue.append(s)
    return total


seed = 690


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, size = 30, 80, 2000
    companies = []
    questions = []
    for _ in range(count):
        ids = list(range(1, size + 1))
        for i in range(size):
            j = i + next_random() % (size - i)
            ids[i], ids[j] = ids[j], ids[i]
        subs = [[] for _ in range(size)]
        for i in range(1, size):
            boss = next_random() % i
            subs[boss].append(ids[i])
        company = []
        for i in range(size):
            importance = next_random() % 201 - 100
            company.append(Employee(ids[i], importance, list(subs[i])))
        companies.append(company)
        questions.append([1 + next_random() % size for _ in range(100)])
    total = 0
    for r in range(rounds):
        for c in range(count):
            for q in range(100):
                got = get_importance(companies[c], questions[c][q])
                total = (total * 31 + got + 1000000 + r) % 1000000007
    print(f"{count * rounds * 100} questions answered, checksum {total}")


main()
