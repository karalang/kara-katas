"""Bench mirror for LeetCode #895 — same algorithm, step for step."""


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
        b = self.buckets.get(f, [])
        b.append(x)
        self.buckets[f] = b

    def pop(self):
        top = self.maxfreq
        b = self.buckets.get(top, [])
        x = b[-1]
        b.pop()
        drained = not b
        self.buckets[top] = b
        self.freq[x] = self.freq.get(x, 0) - 1
        if drained:
            self.maxfreq = top - 1
        return x


def run(rounds, steps):
    checksum = 0
    for r in range(rounds):
        st = FreqStack()
        seed = 12345 + r
        live = 0
        for i in range(steps):
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


if __name__ == "__main__":
    print(run(120, 3000))
