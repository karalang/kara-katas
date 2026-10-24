# LeetCode #937: Reorder Data in Log Files -- bench: two lists and a
# sort. Mirrors reorder_log_files.kara, .c, .rs and go-seq/.


def reorder_log_files(logs):
    letters = []
    digits = []
    for log in logs:
        cut = log.index(" ")
        contents = log[cut + 1:]
        if "0" <= contents[0] <= "9":
            digits.append(log)
        else:
            letters.append((contents, log[:cut], log))
    letters.sort(key=lambda e: (e[0], e[1]))
    return [e[2] for e in letters] + digits


seed = 937


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 200
    count = 200
    lists = []
    for _ in range(count):
        logs = []
        for i in range(100):
            log = chr(97 + next_random() % 26) + str(i)
            digits = next_random() % 2 == 1
            size = 20 + next_random() % 81
            while len(log) + 2 <= size:
                w = 1 + next_random() % 8
                if len(log) + 1 + w > size:
                    w = size - len(log) - 1
                log += " "
                for _ in range(w):
                    if digits:
                        log += chr(48 + next_random() % 10)
                    else:
                        log += chr(97 + next_random() % 5)
            logs.append(log)
        lists.append(logs)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            out = reorder_log_files(lists[(r + i) % count])
            total += len(out)
            for log in out:
                for ch in log:
                    if ch == " ":
                        break
                    check = (check * 131 + ord(ch)) % 1000000007
    print(f"{rounds} rounds over {count} lists of 100 logs: {total} logs, checksum {check}")


main()
