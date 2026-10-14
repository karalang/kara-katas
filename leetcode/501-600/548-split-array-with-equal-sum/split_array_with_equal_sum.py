# LeetCode #548: Split Array with Equal Sum -- Python mirror of the ★
# arm (a set of left sums per middle cut); see split_array_with_equal_sum.kara.


def split_array(nums):
    n = len(nums)
    if n < 7:
        return False
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    for j in range(3, n - 3):
        sums = set()
        for i in range(1, j - 1):
            if prefix[i] == prefix[j] - prefix[i + 1]:
                sums.add(prefix[i])
        for k in range(j + 2, n - 1):
            third = prefix[k] - prefix[j + 1]
            if third == prefix[n] - prefix[k + 1] and third in sums:
                return True
    return False


# ---- test harness ---------------------------------------------------------

seed = 548


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, nums):
    print(f"{name}: {'true' if split_array(nums) else 'false'}")


def planted(size, total):
    nums = []
    for part in range(4):
        if part > 0:
            nums.append(next_random() % 2000001 - 1000000)
        s = 0
        for _ in range(size - 1):
            x = next_random() % 2001 - 1000
            nums.append(x)
            s += x
        nums.append(total - s)
    return nums


def main():
    show("example 1", [1, 2, 1, 2, 1, 2, 1])
    show("example 2", [1, 2, 1, 2, 1, 2, 1, 2])
    show("six values", [0, 0, 0, 0, 0, 0])
    show("seven zeros", [0, 0, 0, 0, 0, 0, 0])
    show("negative parts", [-1, 5, -1, 7, -1, -9, -1])
    show("the cuts are not in the parts", [2, 0, 1, 1, 9, 2, 4, 2, 0])
    show("equal parts but no room for cuts", [1, 1, 1, 1, 1, 1, 1, 1])
    values = yes = h = 0
    for t in range(300):
        n = 1 + next_random() % 30
        spread = 1 if t % 3 == 0 else 2 if t % 3 == 1 else 5
        nums = [next_random() % (2 * spread + 1) - spread for _ in range(n)]
        bit = 1 if split_array(nums) else 0
        values += n
        yes += bit
        h = (h * 31 + bit + 7 * n) % 1000000007
    print(f"300 random arrays: {values} values, {yes} can be split, checksum {h}")
    show("2000 zeros", [0] * 2000)
    wide = [next_random() % 2000001 - 1000000 for _ in range(2000)]
    show("2000 random values", wide)
    show("four planted parts of 499", planted(499, 1000))
    show("199 zeros and a one", [0] * 199 + [1])
    show("200 values swinging", [1000000 if i % 2 == 0 else -1000000 for i in range(200)])


main()
