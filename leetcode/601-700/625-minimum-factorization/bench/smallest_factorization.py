# LeetCode #625: Minimum Factorization -- Python mirror of the Kāra
# bench.
#
# The ★ arm's greedy from the largest digit over the same numbers and
# rounds.


def smallest_factorization(num):
    if num < 10:
        return num
    rest = num
    answer = 0
    place = 1
    for d in range(9, 1, -1):
        while rest % d == 0:
            rest //= d
            answer += d * place
            place *= 10
            if answer > 2147483647:
                return 0
    return answer if rest == 1 else 0


seed = 625


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_numbers(count):
    numbers = []
    for i in range(count):
        if i % 2 == 0:
            product = 1
            for _ in range(1 + next_random() % 10):
                d = 2 + next_random() % 8
                if product * d <= 2147483647:
                    product *= d
            numbers.append(product)
        else:
            high = next_random()
            low = next_random()
            numbers.append(1 + (high * 65536 + low) % 2147483647)
    return numbers


def main():
    count = 200000
    rounds = 50
    numbers = random_numbers(count)
    found = 0
    checksum = 0
    for _ in range(rounds):
        for i in range(count):
            a = smallest_factorization(numbers[i])
            if a != 0:
                found += 1
            checksum = (checksum * 31 + a) % 1000000007
    print(f"{count} numbers, {rounds} rounds: {found} answers, checksum {checksum}")


main()
