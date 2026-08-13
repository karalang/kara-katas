"""LeetCode 256 - Paint House. Python oracle.

Mirrors paint_house.kara algorithm-for-algorithm: three rolling scalars, all
three computed from the previous row before any is assigned.
"""


def min_cost(costs):
    if not costs:
        return 0
    r, b, g = costs[0]
    for i in range(1, len(costs)):
        n_r = costs[i][0] + min(b, g)
        n_b = costs[i][1] + min(r, g)
        n_g = costs[i][2] + min(r, b)
        r, b, g = n_r, n_b, n_g
    return min(r, b, g)


def main():
    cases = [
        ([(17, 2, 17), (16, 16, 5), (14, 3, 19)], "[[17,2,17],[16,16,5],[14,3,19]]"),
        ([], "[]"),
        ([(7, 6, 2)], "[[7,6,2]]"),
        ([(1, 2, 3), (1, 2, 3)], "[[1,2,3],[1,2,3]]"),
        ([(5, 5, 5)] * 4, "[[5,5,5] x4]"),
        ([(1, 100, 100)] * 3, "[[1,100,100] x3]"),
        ([(0, 0, 0)] * 2, "[[0,0,0] x2]"),
        ([(1, 9, 9), (9, 1, 9), (1, 9, 9), (9, 1, 9), (1, 9, 9), (9, 1, 9)], "[alternating x6]"),
        ([(1000000000, 2000000000, 3000000000),
          (3000000000, 1000000000, 2000000000),
          (2000000000, 3000000000, 1000000000)], "[[1e9-scale] x3]"),
    ]
    for c, label in cases:
        print(f"{label} -> {min_cost(c)}")


if __name__ == "__main__":
    main()
