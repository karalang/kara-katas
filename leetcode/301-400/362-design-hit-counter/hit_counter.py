# LeetCode #362: Design Hit Counter -- mirror of hit_counter.kara.
from collections import deque


class HitCounter:
    def __init__(self):
        self.hits = deque()

    def hit(self, timestamp):
        self.hits.append(timestamp)

    def get_hits(self, timestamp):
        while self.hits and self.hits[0] <= timestamp - 300:
            self.hits.popleft()
        return len(self.hits)


def run(label, ops):
    counter = HitCounter()
    answers = []
    for is_hit, t in ops:
        if is_hit:
            counter.hit(t)
        else:
            answers.append(counter.get_hits(t))
    print(f"{label}: [{', '.join(map(str, answers))}]")


def main():
    run("example", [(True, 1), (True, 2), (True, 3), (False, 4), (True, 300), (False, 300), (False, 301)])

    run("no hits", [(False, 1), (False, 1000)])
    run("a hit is counted at its own second", [(True, 5), (False, 5)])
    run("299 seconds later", [(True, 1), (False, 300)])
    run("300 seconds later", [(True, 1), (False, 301)])
    run("many hits in one second", [(True, 7), (True, 7), (True, 7), (False, 7), (False, 306), (False, 307)])
    run("a long gap empties the window", [(True, 1), (True, 2), (False, 2), (False, 100000)])
    run("a sliding window", [(True, 100), (True, 200), (True, 300), (False, 399), (False, 400), (False, 499), (False, 500), (False, 599), (False, 600)])
    run("queries between hits", [(False, 0), (True, 0), (False, 0), (True, 150), (False, 299), (False, 300), (True, 450), (False, 451)])
    run("large timestamps", [(True, 2000000000), (True, 2000000299), (False, 2000000299), (False, 2000000300)])

    seed = 362
    counter = HitCounter()
    t = 1
    queries = 0
    checksum = 0
    for _ in range(20000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        t += (seed // 65536) % 10
        seed = (seed * 1103515245 + 12345) % 2147483648
        if (seed // 65536) % 3 == 0:
            queries += 1
            checksum = (checksum * 31 + counter.get_hits(t)) % 1000000007
        else:
            counter.hit(t)
    print(f"20000 random calls: {queries} queries, checksum {checksum}")


main()
