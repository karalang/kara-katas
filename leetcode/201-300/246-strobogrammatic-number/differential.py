"""Randomized differential for #246 - two independent algorithms, 6,000 cases.

Half the cases are CONSTRUCTED strobogrammatic strings (pairs drawn from the
rotatable set, an odd centre drawn from 0/1/8), and half of those are then
corrupted at one random position. That is deliberate: drawing uniformly from a
digit alphabet makes almost every long string a reject, so the accepting path
would only ever be tested on very short inputs. Constructing valid strings and
then breaking exactly one position puts the hard cases - near-misses that differ
from a legal number in a single character - at every length.

The remaining cases are drawn uniformly over 5 rotatable + 2 forbidden digits,
which covers the "forbidden digit anywhere" path that construction never hits.
"""
def lcg(s): return (s * 1103515245 + 12345) & 2147483647

ROT = {"0": "0", "1": "1", "8": "8", "6": "9", "9": "6"}
PAIRS = [("0", "0"), ("1", "1"), ("8", "8"), ("6", "9"), ("9", "6")]
CENTRE = ["0", "1", "8"]
ALPHA = ["0", "1", "8", "6", "9", "2", "5"]
ALL = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def two_pointer(num):
    lo, hi = 0, len(num) - 1
    while lo <= hi:
        a = num[lo]
        if a not in ROT or ROT[a] != num[hi]:
            return False
        lo += 1
        hi -= 1
    return True

def build_compare(num):
    mapped = []
    for c in num:
        if c not in ROT:
            return False
        mapped.append(ROT[c])
    mapped.reverse()
    return "".join(mapped) == num

def main():
    acc = 0
    s = 1
    disagree = accepts = constructed = corrupted = 0
    for _ in range(6000):
        s = lcg(s)
        n = 1 + (s // 65536) % 8
        s = lcg(s)
        mode = (s // 65536) % 2

        if mode == 0:
            # Uniform draw: exercises the forbidden-digit reject path.
            chars = []
            for _ in range(n):
                s = lcg(s)
                chars.append(ALPHA[(s // 65536) % 7])
        else:
            # Construct a genuinely strobogrammatic string of length n.
            constructed += 1
            chars = [""] * n
            lo, hi = 0, n - 1
            while lo < hi:
                s = lcg(s)
                a, b = PAIRS[(s // 65536) % 5]
                chars[lo], chars[hi] = a, b
                lo += 1
                hi -= 1
            if lo == hi:
                s = lcg(s)
                chars[lo] = CENTRE[(s // 65536) % 3]
            # Half of those get exactly one position corrupted - the near-miss.
            s = lcg(s)
            if (s // 65536) % 2 == 0:
                corrupted += 1
                s = lcg(s)
                pos = (s // 65536) % n
                s = lcg(s)
                chars[pos] = ALL[(s // 65536) % 10]

        num = "".join(chars)
        a, b = two_pointer(num), build_compare(num)
        if a != b:
            disagree += 1
            if disagree <= 3:
                print("MISMATCH", num, a, b)
        if a:
            accepts += 1
        acc = (acc * 131 + (1 if a else 0)) % 1000000007
    print(f"algorithms disagree on {disagree} of 6000 cases")
    print(f"accepted {accepts} of 6000 ({constructed} constructed, {corrupted} then corrupted)")
    print(acc)

main()
