# LeetCode #690: Employee Importance -- depth first through a map.
#
# A mirror of employee_importance.kara (the ★ arm) and its harness.
import sys

sys.setrecursionlimit(10000)


class Employee:
    def __init__(self, id, importance, subordinates):
        self.id = id
        self.importance = importance
        self.subordinates = subordinates


def get_importance(employees, id):
    at = {}
    for i in range(len(employees)):
        at[employees[i].id] = i
    return total(employees, at, id)


def total(employees, at, id):
    e = employees[at[id]]
    s = e.importance
    for sub in e.subordinates:
        s += total(employees, at, sub)
    return s


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def emp(id, importance, subordinates):
    return Employee(id, importance, subordinates)


def main():
    print(f"example 1: {get_importance([emp(1, 5, [2, 3]), emp(2, 3, []), emp(3, 3, [])], 1)}")
    print(f"example 2: {get_importance([emp(1, 2, [5]), emp(5, -3, [])], 5)}")
    print(f"alone: {get_importance([emp(2000, -100, [])], 2000)}")
    gaps = [emp(1999, 4, []), emp(7, -9, [1999, 3]), emp(3, 2, [12]), emp(12, -6, []), emp(1, 100, [])]
    print(f"gaps: 7 -> {get_importance(gaps, 7)}, 3 -> {get_importance(gaps, 3)}, 12 -> {get_importance(gaps, 12)}, 1 -> {get_importance(gaps, 1)}")

    chain = [emp(i, 1, [i + 1] if i < 2000 else []) for i in range(1, 2001)]
    print(f"chain of 2000: from 1 {get_importance(chain, 1)}, from 1001 {get_importance(chain, 1001)}, from 2000 {get_importance(chain, 2000)}")

    flat = [emp(i, i % 201 - 100, []) for i in range(2, 2001)]
    flat.append(emp(1, 0, list(range(2, 2001))))
    print(f"one over 1999: from 1 {get_importance(flat, 1)}, from 2 {get_importance(flat, 2)}")

    seed = [690]
    checksum = 0
    asked = 0
    for _ in range(100):
        n = 1 + next_random(seed) % 300
        ids = list(range(1, 2001))
        for i in range(n):
            j = i + next_random(seed) % (2000 - i)
            ids[i], ids[j] = ids[j], ids[i]
        subs = [[] for _ in range(n)]
        for i in range(1, n):
            if next_random(seed) % 10 != 0:
                boss = next_random(seed) % i
                subs[boss].append(ids[i])
        company = []
        for i in range(n):
            company.append(emp(ids[i], next_random(seed) % 201 - 100, list(subs[i])))
        for _ in range(20):
            who = ids[next_random(seed) % n]
            checksum = (checksum * 31 + get_importance(company, who) + 1000000) % 1000000007
            asked += 1
    print(f"{asked} random questions: checksum {checksum}")


main()
