# LeetCode #2451: Odd String Difference -- Python mirror of the ★ arm
# (odd.kara): the common difference array read off the first three
# words, and the word whose array is not it.


def differences(word):
    return [ord(word[j]) - ord(word[j - 1]) for j in range(1, len(word))]


def odd_string(words):
    a = differences(words[0])
    b = differences(words[1])
    c = differences(words[2])
    common = a if a == b or a == c else b
    for w in words:
        if differences(w) != common:
            return w
    return words[0]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_steps(length, reach):
    steps = []
    at = low = high = 0
    for _ in range(1, length):
        step = next_random() % (2 * reach + 1) - reach
        if max(high, at + step) - min(low, at + step) > 25:
            step = 0
        steps.append(step)
        at += step
        low = min(low, at)
        high = max(high, at)
    return steps


def word_of(steps):
    at = low = high = 0
    for s in steps:
        at += s
        low = min(low, at)
        high = max(high, at)
    first = -low + next_random() % (26 - (high - low))
    letters = [97 + first]
    code = first
    for s in steps:
        code += s
        letters.append(97 + code)
    return bytes(letters).decode()


def random_case(count, length, odd, reach):
    common = random_steps(length, reach)
    other = random_steps(length, reach)
    while other == common:
        other = random_steps(length, reach)
    return [word_of(other if i == odd else common) for i in range(count)]


def main():
    global seed
    print(f"example 1: {odd_string(['adc', 'wzy', 'abc'])}")
    print(f"example 2: {odd_string(['aaa', 'bob', 'ccc', 'ddd'])}")
    print(f"odd first: {odd_string(['az', 'ab', 'bc', 'yz'])}")
    print(f"odd last: {odd_string(['ab', 'bc', 'yz', 'za'])}")
    seed = 2451
    for odd in [0, 57, 99]:
        words = random_case(100, 20, odd, 3)
        answer = odd_string(words)
        print(f"100 of 20, odd at {odd}: {answer}, found at {words.index(answer)}")
    check = 0
    for _ in range(3000):
        count = 3 + next_random() % 6
        length = 2 + next_random() % 5
        odd = next_random() % count
        words = random_case(count, length, odd, 2)
        answer = odd_string(words)
        check = (check * 31 + words.index(answer) + 1) % 1000000007
    print(f"3000 random: checksum {check}")


main()
