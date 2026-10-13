# Benchmark for #506 in Python: the ★ arm (the athletes sorted by score);
# see ../find_relative_ranks.kara.


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


seed = 506


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 500 lists of 10,000 athletes (the problem's most), all different
    # scores from 0 to 10^6 (the j-th is j * 100 plus less than 100,
    # shuffled), built once. Then each list is ranked once, the length
    # of every rank folded into a checksum.
    lists = 500
    n = 10000
    all_scores = []
    for _ in range(lists):
        score = []
        for j in range(n):
            score.append(j * 100 + next_random() % 100)
        k = n - 1
        while k > 0:
            other = next_random() % (k + 1)
            score[k], score[other] = score[other], score[k]
            k -= 1
        all_scores.append(score)
    letters = 0
    checksum = 0
    for c in range(lists):
        for rank in find_relative_ranks(all_scores[c]):
            letters += len(rank)
            checksum = (checksum * 31 + len(rank)) % 1000000007
    print(f"{lists} lists of {n} athletes: {letters} characters, checksum {checksum}")


main()
