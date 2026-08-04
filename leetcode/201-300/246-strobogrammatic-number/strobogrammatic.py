"""LeetCode 246 - Strobogrammatic Number (reference oracle).

A number is strobogrammatic if it reads the same after rotating the page 180
degrees. Rotation does two things at once: each digit turns into another digit,
and the whole string reverses. Only five digits survive a rotation -
0->0, 1->1, 8->8, 6->9, 9->6 - and 2,3,4,5,7 turn into nothing legible, so a
single occurrence of one is enough to fail.

Two-pointer form: for every pair (l, r) closing in from the ends, rot(num[l])
must equal num[r]. The middle character of an odd-length number pairs with
ITSELF, which is why 0/1/8 may sit there but 6 and 9 may not.
"""

ROT = {"0": "0", "1": "1", "8": "8", "6": "9", "9": "6"}


def is_strobogrammatic(num):
    lo = 0
    hi = len(num) - 1
    while lo <= hi:
        a = num[lo]
        b = num[hi]
        if a not in ROT or ROT[a] != b:
            return False
        lo += 1
        hi -= 1
    return True


def report(num):
    print(f"{num} : {'true' if is_strobogrammatic(num) else 'false'}")


def main():
    # Single digits: only 0, 1 and 8 survive rotating in place.
    report("0")
    report("1")
    report("8")
    report("6")
    report("9")
    report("2")

    # LeetCode's examples.
    report("69")
    report("88")
    report("962")

    # Pairs: the rotation must land on the OTHER end.
    report("96")
    report("11")
    report("18")
    report("00")

    # Odd length - the centre pairs with itself, so 6/9 cannot sit there.
    report("101")
    report("181")
    report("609")
    report("916")
    report("619")
    report("689")

    # Longer, and the near-miss that catches a reverse-only implementation.
    report("6009")
    report("6996")
    report("1001")
    report("88088")
    report("69896")

    # Any forbidden digit anywhere is fatal, even surrounded by valid pairs.
    report("10501")
    report("6739")


if __name__ == "__main__":
    main()
