def min_number_of_frogs(s, lo, hi):
    heard = [0, 0, 0, 0, 0]
    most = 0
    for j in range(lo, hi):
        i = "croak".find(s[j])
        if i < 0:
            return -1
        heard[i] += 1
        if i > 0 and heard[i] > heard[i - 1]:
            return -1
        most = max(most, heard[0] - heard[4])
    return most if heard[0] == heard[4] else -1


def main():
    seed = 1419
    word = "croak"
    pool = []
    for _ in range(1000):
        croaking = []
        started = 0
        while started < 100 or croaking:
            seed = (seed * 1103515245 + 12345) % 2147483648
            r = seed // 65536
            if started < 100 and (not croaking or r % 3 == 0):
                pool.append("c")
                croaking.append(1)
                started += 1
            else:
                i = r // 3 % len(croaking)
                pool.append(word[croaking[i]])
                croaking[i] += 1
                if croaking[i] == 5:
                    croaking[i] = croaking[-1]
                    croaking.pop()
    text = "".join(pool)
    check = 0
    for _ in range(500):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = 500 * (seed // 65536 % 801)
        check = (check * 131 + min_number_of_frogs(text, start, start + 100000) + 1) % 1000000007
    print(f"500 windows of 10^5 letters: checksum {check}")


main()
