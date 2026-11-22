# LeetCode #2734: Lexicographically Smallest String After Substring
# Operation -- the bench (smallest.kara in Python): the run from the
# first letter that is not an 'a' up to the next 'a' moved back a letter,
# edited in a bytearray.


def smallest_string(s):
    b = bytearray(s)
    n = len(b)
    i = 0
    while i < n and b[i] == 97:
        i += 1
    if i == n:
        b[n - 1] = 122
    else:
        while i < n and b[i] != 97:
            b[i] -= 1
            i += 1
    return bytes(b)


seed = 2734


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 100, 100000, 20
    words = []
    for _ in range(count):
        lead = next_random() % (n // 2)
        word = bytearray()
        for k in range(n):
            if k < lead or next_random() % 5000 == 0:
                word.append(97)
            else:
                word.append(98 + next_random() % 25)
        words.append(bytes(word))
    total = 0
    check = 0
    for r in range(rounds):
        for word in words:
            answer = smallest_string(word)
            moved = 0
            for k in range(len(answer)):
                if answer[k] != word[k]:
                    moved += 1
            total += moved
            check = (check * 31 + moved + (answer[len(answer) // 2] - 97) + r) % 1000000007
    print(f"{count} words of {n} letters, {rounds} rounds: letters moved sum to {total}, checksum {check}")


main()
