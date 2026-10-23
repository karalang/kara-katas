# LeetCode #900: RLE Iterator -- Python mirror of the runs-used-up-in-place
# solution in rle_iterator.kara, with the same test harness.
#
# Keep the encoding and the place of the run being read. To use up n
# terms, step past every run whose count is less than what is still
# needed, taking its count off; then take the rest off the count of the
# run reached and answer its value. O(length + calls).


class RLEIterator:
    def __init__(self, encoding):
        self.encoding = encoding
        self.i = 0

    def next(self, n):
        need = n
        while self.i < len(self.encoding) and self.encoding[self.i] < need:
            need -= self.encoding[self.i]
            self.i += 2
        if self.i >= len(self.encoding):
            return -1
        self.encoding[self.i] -= need
        return self.encoding[self.i + 1]


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a random number from 0 to below `limit`, up to 2^30
def random_below(limit):
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % limit


def answers(encoding, calls):
    it = RLEIterator(encoding)
    return [it.next(n) for n in calls]


def join(v):
    return ", ".join(str(x) for x in v)


def show(encoding, calls):
    e = join(encoding)
    c = join(calls)
    got = join(answers(list(encoding), calls))
    print(f"encoding = [{e}], next({c}) -> {got}")


def checksum(got, check):
    for x in got:
        check = (check * 1000003 + x + 1) % 1000000007
    return check


def main():
    global seed
    show([3, 8, 0, 9, 2, 5], [2, 1, 1, 2])
    show([1, 7], [1, 1])
    show([0, 1, 0, 2], [1])
    show([5, 4], [5, 1])
    show([3, 1], [4, 1])
    show([2, 1, 3, 2, 1, 3], [3, 1, 1, 1, 1])
    show([1, 6, 0, 6, 1, 6], [2, 1])
    show([1000000000, 7, 1000000000, 9], [1000000000, 1, 999999999, 1])
    # random cases: up to 500 runs, counts up to 3 (zeros among them), up
    # to 1000 or up to 10^9, values up to 10^9, and up to 1000 calls that
    # each ask for up to a quarter of the largest count
    seed = 900
    check = 0
    calls_in_all = 0
    minus = 0
    for c in range(300):
        runs = 1 + next_random() % 500
        most = 4 if c % 3 == 0 else 1001 if c % 3 == 1 else 1000000001
        encoding = []
        for _ in range(runs):
            encoding.append(random_below(most))
            encoding.append(random_below(1000000001))
        ncalls = 1 + next_random() % 1000
        calls = [1 + random_below(most // 4 + 1) for _ in range(ncalls)]
        got = answers(encoding, calls)
        minus += sum(1 for x in got if x == -1)
        check = checksum(got, check)
        calls_in_all += ncalls
    print(f"300 cases, {calls_in_all} calls, {minus} answered -1: checksum {check}")
    # LeetCode's largest: 500 runs of 10^9 terms asked for 10^9 at a time,
    # a run and a term over each time; and 500 runs of one term each,
    # asked for one at a time
    big = []
    ones = []
    for j in range(500):
        big.append(1000000000)
        big.append(j * 1000)
        ones.append(1)
        ones.append(random_below(1000000001))
    big_calls = [1000000001] * 1000
    one_calls = [1] * 1000
    print(f"500 runs of 10^9, 1000 calls of 10^9 + 1 -> checksum {checksum(answers(big, big_calls), 0)}")
    print(f"500 runs of 1, 1000 calls of 1 -> checksum {checksum(answers(ones, one_calls), 0)}")


main()
