"""LeetCode #895: Maximum Frequency Stack — the oracle mirror.

Same algorithm as the Kara version, element for element: a frequency count per
value, a per-frequency stack of the values that reached it, and a running
maximum. `pop` takes the last element of the top bucket, which is the most
recent among the most frequent.
"""


class FreqStack:
    def __init__(self):
        self.freq = {}
        self.buckets = {}
        self.maxfreq = 0

    def push(self, x):
        f = self.freq.get(x, 0) + 1
        self.freq[x] = f
        if f > self.maxfreq:
            self.maxfreq = f
        self.buckets.setdefault(f, []).append(x)

    def pop(self):
        b = self.buckets[self.maxfreq]
        x = b[-1]
        b.pop()
        self.freq[x] = self.freq.get(x, 0) - 1
        if not b:
            self.maxfreq -= 1
        return x


def stress():
    """Mirror of the Kara stress: an LCG feeds pushes, every third step pops."""
    st = FreqStack()
    seed = 12345
    live = 0
    checksum = 0
    for i in range(600):
        seed = (seed * 1103515245 + 12345) % 2147483648
        if i % 3 == 2 and live > 0:
            checksum += st.pop() * (i % 7 + 1)
            live -= 1
        else:
            st.push(seed % 12)
            live += 1
    while live > 0:
        checksum += st.pop()
        live -= 1
    return checksum


def main():
    st = FreqStack()
    for v in (5, 7, 5, 7, 4, 5):
        st.push(v)
    for _ in range(4):
        print(st.pop())
    print(stress())


if __name__ == "__main__":
    main()
