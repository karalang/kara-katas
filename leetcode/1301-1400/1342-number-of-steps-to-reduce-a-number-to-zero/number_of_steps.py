# LeetCode #1342: Number of Steps to Reduce a Number to Zero -- Python
# mirror of the ★ arm: halve an even number, take one from an odd one,
# count the steps.


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
    print(" ".join(str(number_of_steps(x)) for x in (14, 8, 123, 0, 1, 1000000, 524287)))
    total = 0
    check = 0
    for num in range(1000001):
        steps = number_of_steps(num)
        total += steps
        check = (check * 131 + steps) % 1000000007
    print(f"0 to 10^6: {total} steps, checksum {check}")


main()
