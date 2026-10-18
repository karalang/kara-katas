# LeetCode #703 bench: the heap arm in Python. See the .kara twin for the
# workload.

seed = 703


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []
        for x in nums:
            self.add(x)

    def add(self, val):
        h = self.heap
        if len(h) < self.k:
            h.append(val)
            i = len(h) - 1
            while i > 0:
                parent = (i - 1) // 2
                if h[parent] <= h[i]:
                    break
                h[parent], h[i] = h[i], h[parent]
                i = parent
        elif val > h[0]:
            h[0] = val
            n = len(h)
            i = 0
            while True:
                left = 2 * i + 1
                right = left + 1
                least = i
                if left < n and h[left] < h[least]:
                    least = left
                if right < n and h[right] < h[least]:
                    least = right
                if least == i:
                    break
                h[least], h[i] = h[i], h[least]
                i = least
        return h[0]


def main():
    checksum = 0
    changes = 0
    for _ in range(5):
        for stream in range(10):
            k = 50 * (stream + 1)
            price = 100000
            nums = []
            for _ in range(1000):
                price += next_random() % 201 - 90
                nums.append(price)
            s = KthLargest(k, nums)
            last = 0
            for _ in range(200000):
                price += next_random() % 201 - 90
                answer = s.add(price)
                if answer != last:
                    changes += 1
                last = answer
                checksum = (checksum * 31 + answer) % 1000000007
    print(f"5 rounds of 10 streams of 200000 prices: answer changed {changes} times, checksum {checksum}")


main()
