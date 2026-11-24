# LeetCode #1342 bench in Python: the ★ arm (halve an even number, take
# one from an odd one, count the steps) on the same 5 passes over 10^6 + 1
# numbers.


def number_of_steps(num):
    steps = 0
    while num > 0:
        if num % 2 == 0:
            num //= 2
        else:
            num -= 1
        steps += 1
    return steps


def main():
    check = 0
    for pass_ in range(5):
        for x in range(1000001):
            check = (check * 31 + number_of_steps((x + check) % 1000001) + pass_) % 1000000007
    print(f"5 passes over 10^6 + 1 numbers: checksum {check}")


main()
