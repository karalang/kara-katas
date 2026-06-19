# LeetCode #46 bench mirror — Python, the used-array mutable-path backtracker (star).
#
# Mirrors bench/permutations.kara: a DFS that picks any still-unused element (tracked by a
# `used` bool list) alongside a mutable path, snapshotting into a list-of-lists at each leaf.
# Same workload (TOTAL permutations of a fixed n=7 array, one slot punched per iteration) and
# the same position-weighted checksum as every other mirror. Slow lane — the interpreted
# reference time.

TOTAL = 300
MODULUS = 1000000007
N = 7


def backtrack(nums, used, path, out):
    n = len(nums)
    if len(path) == n:
        out.append(path.copy())
        return
    for i in range(n):
        if not used[i]:
            used[i] = True
            path.append(nums[i])
            backtrack(nums, used, path, out)
            path.pop()
            used[i] = False


def permute(nums):
    used = [False] * len(nums)
    path = []
    out = []
    backtrack(nums, used, path, out)
    return out


def main():
    nums = [b + 1 for b in range(N)]

    acc = 0
    for k in range(TOTAL):
        nums[k % N] = 1 + (k % 9)
        perms = permute(nums)

        sig = 0
        for perm in perms:
            s = 0
            for i in range(len(perm)):
                s += perm[i] * (i + 1)
            sig = (sig * 31 + s) % MODULUS
        sig = (sig + len(perms)) % MODULUS
        acc = (acc * 131 + sig) % MODULUS

    print(acc)


if __name__ == "__main__":
    main()
