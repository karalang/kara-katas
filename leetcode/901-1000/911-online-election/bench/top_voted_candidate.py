# LeetCode #911: Online Election -- bench program, Python.
#
# The leader after every vote, and a binary search for the time, on one
# election of 1,000,000 votes among 1,000 people, built once. Each query
# asks for the leader at a random time and folds the answer into a
# checksum; 2,000,000 queries.


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


seed = 911


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 1000000
    queries = 2000000
    persons = []
    times = []
    at = 0
    for _ in range(n):
        persons.append(next_random() % 1000)
        times.append(at)
        at += 1 + next_random() % 1000
    e = TopVotedCandidate(persons, times)
    check = 0
    for _ in range(queries):
        high = next_random()
        t = (high * 32768 + next_random()) % at
        check = (check * 31 + e.q(t)) % 1000000007
    print(f"{n} votes, {queries} queries: checksum {check}")


main()
