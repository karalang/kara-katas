# LeetCode #412: Fizz Buzz -- mirror of fizz_buzz.kara (test each case).


def fizz_buzz(n):
    answer = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            answer.append("FizzBuzz")
        elif i % 3 == 0:
            answer.append("Fizz")
        elif i % 5 == 0:
            answer.append("Buzz")
        else:
            answer.append(str(i))
    return answer


seed = 412


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(n):
    print(f"{n}: {' '.join(fizz_buzz(n))}")


show(1)
show(3)
show(5)
show(15)
show(16)
show(31)
words = 0
numbers = 0
checksum = 0
for _ in range(100):
    hi = step()
    lo = step()
    n = 1 + (hi * 32768 + lo) % 10000
    for entry in fizz_buzz(n):
        b = entry.encode()
        if b[0] >= 65:
            words += 1
        else:
            numbers += 1
        for x in b:
            checksum = (checksum * 31 + x) % 1000000007
print(f"100 random n: {words} words, {numbers} numbers, checksum {checksum}")
