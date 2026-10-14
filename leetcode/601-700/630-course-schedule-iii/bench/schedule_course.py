# LeetCode #630: Course Schedule III -- Python mirror of the Kāra
# bench.
#
# The ★ arm's greedy over the same inputs and rounds: the courses
# sorted by last day into a new list, and a heap of the negated
# durations taken.

import heapq


def schedule_course(courses):
    order = sorted(courses, key=lambda c: c[1])
    taken = []
    time = 0
    for duration, last in order:
        time += duration
        heapq.heappush(taken, -duration)
        if time > last:
            time += heapq.heappop(taken)
    return len(taken)


seed = 630


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs = 20
    rounds = 200
    all_inputs = []
    for _ in range(inputs):
        longest = 10 + next_random() % 991
        courses = []
        for _ in range(10000):
            duration = 1 + next_random() % longest
            last = 1 + next_random() % 10000
            courses.append([duration, last])
        all_inputs.append(courses)
    total = 0
    checksum = 0
    for r in range(rounds):
        c = schedule_course(all_inputs[(r * 7) % inputs])
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"{inputs} inputs, {rounds} rounds: total {total}, checksum {checksum}")


main()
