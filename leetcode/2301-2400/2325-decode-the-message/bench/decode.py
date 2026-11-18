# LeetCode #2325: Decode the Message -- the bench, the ★ arm in Python.
# One walk over the key's bytes fills a table of 26, each letter's first
# appearance given the next letter of the alphabet, and the message is
# read through it, spaces kept. O(|key| + |message|).


def decode_message(key, message):
    table = [0] * 26
    nxt = 97
    for b in key.encode():
        if b != 32 and table[b - 97] == 0:
            table[b - 97] = nxt
            nxt += 1
    return "".join(" " if b == 32 else chr(table[b - 97]) for b in message.encode())


seed = 2325


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter():
    roll = next_random() % 27
    return " " if roll == 26 else chr(97 + roll)


def main():
    keys = []
    messages = []
    for _ in range(100):
        key = "".join(letter() for _ in range(1974)) + "abcdefghijklmnopqrstuvwxyz"
        keys.append(key)
        messages.append("".join(letter() for _ in range(2000)))
    check = 0
    for p in range(1000):
        for k in range(100):
            decoded = decode_message(keys[k], messages[k]).encode()
            check = (check * 31 + decoded[p % 2000] + decoded[(7 * p + k) % 2000]) % 1000000007
            keys[k] = keys[k][1:] + keys[k][0]
    print(f"1000 passes over 100 keys and messages of 2000: checksum {check}")


main()
