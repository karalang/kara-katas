# LeetCode #506: Relative Ranks -- Python mirror of the ★ arm (the
# athletes sorted by score, highest first); see find_relative_ranks.kara.


def find_relative_ranks(score):
    n = len(score)
    order = sorted(range(n), key=lambda i: -score[i])
    answer = [""] * n
    for place in range(n):
        if place == 0:
            answer[order[place]] = "Gold Medal"
        elif place == 1:
            answer[order[place]] = "Silver Medal"
        elif place == 2:
            answer[order[place]] = "Bronze Medal"
        else:
            answer[order[place]] = f"{place + 1}"
    return answer


# ---- test harness ---------------------------------------------------------

seed = 506


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(name, score):
    print(f"{name}: {fmt(score)} -> {fmt(find_relative_ranks(score))}")


def main():
    show("example 1", [5, 4, 3, 2, 1])
    show("example 2", [10, 3, 8, 9, 4])
    show("one athlete", [7])
    show("two", [1, 2])
    show("rising", [1, 2, 3, 4, 5, 6])
    show("the extremes", [0, 1000000, 500000, 999999])
    # 300 random lists of 1 to 30 different scores: the j-th of n is
    # j * spread plus less than spread, shuffled, with spread 3, 1,000
    # or 33,000 in turn.
    count = 300
    athletes = 0
    checksum = 0
    for c in range(count):
        n = 1 + next_random() % 30
        spread = 3 if c % 3 == 0 else 1000 if c % 3 == 1 else 33000
        score = []
        for j in range(n):
            score.append(j * spread + next_random() % spread)
        k = n - 1
        while k > 0:
            other = next_random() % (k + 1)
            score[k], score[other] = score[other], score[k]
            k -= 1
        for rank in find_relative_ranks(score):
            athletes += 1
            for ch in rank:
                checksum = (checksum * 31 + ord(ch)) % 1000000007
    print(f"{count} random lists: {athletes} athletes, checksum {checksum}")


main()
