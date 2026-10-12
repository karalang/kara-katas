# Benchmark for #412: mirror of fizz_buzz.kara (test each case).
import sys


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


def main():
    calls = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    total = 0
    checksum = 0
    for _ in range(calls):
        n = 9000 + step() % 1001
        length = sum(len(s) for s in fizz_buzz(n))
        total += length
        checksum = (checksum * 31 + length) % 1000000007
    print(f"{calls} calls: {total} bytes, checksum {checksum}")


main()
