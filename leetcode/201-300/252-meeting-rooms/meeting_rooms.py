"""LeetCode 252 - Meeting Rooms. Python oracle.

Mirrors meeting_rooms.kara algorithm-for-algorithm: sort by start, then a single
adjacent comparison with a STRICT `<`, so a meeting ending exactly as the next
begins is attendable.
"""


def can_attend_all(intervals):
    s = sorted(intervals, key=lambda x: x[0])
    for i in range(1, len(s)):
        if s[i][0] < s[i - 1][1]:
            return False
    return True


def main():
    cases = [
        ([(0, 30), (5, 10), (15, 20)], "[[0,30],[5,10],[15,20]]"),
        ([(7, 10), (2, 4)], "[[7,10],[2,4]]"),
        ([], "[]"),
        ([(1, 5)], "[[1,5]]"),
        ([(1, 5), (5, 10)], "[[1,5],[5,10]]"),
        ([(1, 10), (2, 3)], "[[1,10],[2,3]]"),
        ([(5, 10), (1, 5)], "[[5,10],[1,5]]"),
        ([(1, 3), (3, 5), (5, 7), (7, 9)], "[[1,3],[3,5],[5,7],[7,9]]"),
        ([(1, 2), (1, 2)], "[[1,2],[1,2]]"),
        ([(1, 4), (2, 5), (3, 6)], "[[1,4],[2,5],[3,6]]"),
    ]
    for iv, label in cases:
        print(f"{label} -> {'true' if can_attend_all(iv) else 'false'}")


if __name__ == "__main__":
    main()
