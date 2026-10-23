# LeetCode #911: Online Election -- Python mirror of the leader after every
# vote in top_voted_candidate.kara, with the same test harness.


class TopVotedCandidate:
    def __init__(self, persons, times):
        n = len(persons)
        count = [0] * n
        self.leaders = []
        leader = persons[0]
        for i in range(n):
            p = persons[i]
            count[p] += 1
            if count[p] >= count[leader]:
                leader = p
            self.leaders.append(leader)
        self.times = list(times)

    def q(self, t):
        lo = 0
        hi = len(self.times)
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.times[mid] <= t:
                lo = mid
            else:
                hi = mid
        return self.leaders[lo]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def join(v):
    return ",".join(str(x) for x in v)


def show(persons, times, queries):
    e = TopVotedCandidate(persons, times)
    answers = [e.q(t) for t in queries]
    print(f"persons = [{join(persons)}], times = [{join(times)}]: q({join(queries)}) -> {join(answers)}")


def election(n, among, gap, asked):
    persons = []
    times = []
    t = next_random() % (gap + 1)
    for _ in range(n):
        persons.append(next_random() % among)
        times.append(t)
        t += 1 + next_random() % gap
    e = TopVotedCandidate(persons, times)
    check = 0
    for _ in range(asked):
        ask = times[0] + next_random() % (t - times[0])
        check = (check * 1000003 + e.q(ask)) % 1000000007
    return check


def main():
    global seed
    show([0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30], [3, 12, 25, 15, 24, 8])
    show([0], [7], [7, 1000000000])
    show([0, 1], [1, 2], [1, 2, 3])
    show([2, 2, 1, 1, 0, 0, 1], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6])
    show([3, 1, 2, 0], [10, 20, 30, 1000000000], [15, 25, 35, 999999999, 1000000000])
    seed = 911
    check = 0
    for c in range(300):
        n = 1 + next_random() % 500
        among = min(2, n) if c % 3 == 0 else min(10, n) if c % 3 == 1 else n
        gap = 3 if c % 4 == 0 else 1000 if c % 4 == 1 else 1000000
        check = (check * 31 + election(n, among, gap, 30)) % 1000000007
    print(f"300 elections: checksum {check}")
    print(f"5000 votes among 5000, 10000 queries: checksum {election(5000, 5000, 199999, 10000)}")
    print(f"5000 votes among 3, 10000 queries: checksum {election(5000, 3, 199999, 10000)}")


main()
