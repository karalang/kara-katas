# LeetCode #2468: Split Message Based on Limit -- the bench, the ★ arm in
# Python: the least part count found with a running sum of the counts'
# digits, then the parts cut in order.


def digits(v):
    return len(str(v))


def split_message(message, limit):
    n = len(message)
    digit_sum = 0
    parts = 0
    b = 1
    while 3 + 2 * digits(b) < limit:
        digit_sum += digits(b)
        if b * (limit - 3 - digits(b)) - digit_sum >= n:
            parts = b
            break
        b += 1
    out = []
    if parts == 0:
        return out
    at = 0
    for a in range(1, parts + 1):
        room = limit - 3 - digits(a) - digits(parts)
        end = min(at + room, n)
        out.append(f"{message[at:end]}<{a}/{parts}>")
        at = end
    return out


seed = 2468


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 messages of 10^4 lowercase letters and spaces built once; then
    # 2600 passes, each choosing every message's limit, from 12 to 211,
    # from the checksum so far, then splitting it and folding the part
    # count, the last part's length and the pass into the checksum
    letters = "abcdefghijklmnopqrstuvwxyz "
    messages = []
    for _ in range(20):
        messages.append("".join(letters[next_random() % 27] for _ in range(10000)))
    check = 0
    for p in range(2600):
        for m in messages:
            limit = 12 + check % 200
            parts = split_message(m, limit)
            last = len(parts[-1])
            check = (check * 31 + len(parts) + last + p) % 1000000007
    print(f"2600 passes over 20 messages of 10^4: checksum {check}")


main()
