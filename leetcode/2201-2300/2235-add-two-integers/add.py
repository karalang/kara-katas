# LeetCode #2235: Add Two Integers -- the mirror of add.kara: the two
# added with `+`.


def sum_of(num1, num2):
    return num1 + num2


def show(num1, num2):
    print(f"{num1} + {num2} = {sum_of(num1, num2)}")


def main():
    show(12, 5)
    show(-10, 4)
    show(-100, -100)
    show(100, 100)
    show(0, 0)
    show(-7, 7)
    show(-1, 1)
    check = 0
    negative = 0
    zero = 0
    for num1 in range(-100, 101):
        for num2 in range(-100, 101):
            s = sum_of(num1, num2)
            check = (check * 31 + s + 200) % 1000000007
            if s < 0:
                negative += 1
            elif s == 0:
                zero += 1
    print(f"40401 pairs: checksum {check}, {negative} negative, {zero} zero")


main()
