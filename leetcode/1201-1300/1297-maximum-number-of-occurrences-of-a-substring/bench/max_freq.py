# LeetCode #1297 bench: the ★ arm (one window of minSize letters slid along
# the string, each with few enough distinct letters counted in a dict by its
# text) over 10 strings of 10^5 letters over the first 2 to 6 letters, built
# once; then 20 passes, each setting one letter of every string and its limits
# from the checksum so far, answering it, and folding the answer into the
# checksum.


def max_freq(s, max_letters, min_size, max_size):
    n = len(s)
    letters = [0] * 26
    distinct = 0
    seen = {}
    best = 0
    for i in range(n):
        add = ord(s[i]) - 97
        if letters[add] == 0:
            distinct += 1
        letters[add] += 1
        if i >= min_size:
            gone = ord(s[i - min_size]) - 97
            letters[gone] -= 1
            if letters[gone] == 0:
                distinct -= 1
        if i + 1 >= min_size and distinct <= max_letters:
            window = s[i + 1 - min_size:i + 1]
            times = seen.get(window, 0) + 1
            seen[window] = times
            if times > best:
                best = times
    return best


seed = 1297


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    texts = []
    for t in range(10):
        alphabet = 2 + t % 5
        texts.append(bytearray(97 + next_random() % alphabet for _ in range(100000)))
    check = 0
    for p in range(20):
        for t in range(len(texts)):
            texts[t][check % 100000] = 97 + check % (2 + t % 5)
            s = texts[t].decode()
            min_size = 1 + check % 26
            max_letters = 1 + (check // 26) % 26
            check = (check * 31 + max_freq(s, max_letters, min_size, min_size) + p) % 1000000007
    print(f"20 passes over 10 strings of 10^5: checksum {check}")


main()
