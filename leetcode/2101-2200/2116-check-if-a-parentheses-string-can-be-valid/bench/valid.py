# LeetCode #2116: Check if a Parentheses String Can Be Valid -- the
# benchmark, the same algorithm as valid.kara: two greedy passes over the
# bytes.
import sys


def can_be_valid(s, locked):
    n = len(s)
    if n % 2 == 1:
        return False
    open_ = 0
    for i in range(n):
        if s[i] == 40 or locked[i] == 48:
            open_ += 1
        else:
            open_ -= 1
            if open_ < 0:
                return False
    close = 0
    for i in range(n - 1, -1, -1):
        if s[i] == 41 or locked[i] == 48:
            close += 1
        else:
            close -= 1
            if close < 0:
                return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2116]
    strings = []
    locks = []
    n = 50000
    for k in range(64):
        flip = next_random(seed) % n if next_random(seed) % 2 == 0 else -1
        s = bytearray()
        locked = bytearray()
        open_ = 0
        for i in range(n):
            if open_ == 0:
                up = True
            elif open_ == n - i:
                up = False
            else:
                up = next_random(seed) % 2 == 0
            open_ += 1 if up else -1
            if i == flip:
                up = not up
            s.append(40 if up else 41)
            unlocked = next_random(seed) % 4 == 0 and k % 2 == 0
            locked.append(48 if unlocked else 49)
        strings.append(s)
        locks.append(locked)
    valid = 0
    check = 0
    for rnd in range(40):
        for a in range(64):
            strings[a] += b"()"
            locks[a] += b"11"
            got = can_be_valid(strings[a], locks[a])
            if got:
                valid += 1
            check = (check * 31 + (rnd + a if got else 1)) % 1000000007
    print(f"2560 solves: {valid} can be valid, checksum {check}")


main()
