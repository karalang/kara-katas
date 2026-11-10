# LeetCode #1103: Distribute Candies to People -- the bench in Python:
# the ★ arm (gifts of 1, 2, 3, ... in turn, the last whatever is left)
# over 64 problems, each round moving every problem's candies.


def distribute_candies(candies, num_people):
    people = [0] * num_people
    left = candies
    gift = 1
    while left > 0:
        given = min(gift, left)
        people[(gift - 1) % num_people] += given
        left -= given
        gift += 1
    return people


seed = 1103


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    problems = []
    for _ in range(64):
        hi = next_random()
        candies = (hi * 32768 + next_random()) % 1000000000 + 1
        n = next_random() % 1000 + 1
        problems.append((candies, n))
    total = 0
    check = 0
    for rnd in range(200):
        for j in range(len(problems)):
            candies, n = problems[j]
            candies = (candies + rnd * 7919 + j * 104729) % 1000000000 + 1
            problems[j] = (candies, n)
            people = distribute_candies(candies, n)
            total += people[0] + people[n - 1]
            for c in people:
                check = (check * 31 + c + 1) % 1000000007
    print(f"200 rounds over 64 problems of up to 10^9 candies: first and last people hold {total}, checksum {check}")


main()
