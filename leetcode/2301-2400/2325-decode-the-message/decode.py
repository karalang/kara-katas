# LeetCode #2325: Decode the Message -- the ★ arm in Python. One walk over
# the key fills a table of 26: each letter's first appearance is given
# the next letter of the alphabet. The message is then read through the
# table, spaces kept. O(|key| + |message|).


def decode_message(key, message):
    table = [0] * 26
    nxt = ord("a")
    for b in key.encode():
        if b != ord(" ") and table[b - ord("a")] == 0:
            table[b - ord("a")] = nxt
            nxt += 1
    return "".join(" " if b == ord(" ") else chr(table[b - ord("a")]) for b in message.encode())


seed = 2325


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_key():
    letters = [chr(ord("a") + i) for i in range(26)]
    for i in range(25, 0, -1):
        j = next_random() % (i + 1)
        letters[i], letters[j] = letters[j], letters[i]
    key = ""
    for i in range(26):
        key += letters[i]
        roll = next_random() % 6
        if roll == 0:
            key += " "
        elif roll == 1:
            key += letters[next_random() % (i + 1)]
    return key


def random_message(length):
    message = ""
    for _ in range(length):
        roll = next_random() % 27
        message += " " if roll == 26 else chr(ord("a") + roll)
    return message


def main():
    print(decode_message("the quick brown fox jumps over the lazy dog", "vkbs bs t suepuv"))
    print(decode_message("eljuxhpwnyrdgtqkviszcfmabo", "zwx hnfx lqantp mnoeius ycgk vcnjrdb"))
    print(decode_message("abcdefghijklmnopqrstuvwxyz", "hello world"))
    print(decode_message("zyxwvutsrqponmlkjihgfedcba", "svool dliow"))
    print(f"[{decode_message('a b c d e f g h i j k l m n o p q r s t u v w x y z', '   ')}]")
    check = 0
    letters = 0
    for _ in range(2000):
        key = random_key()
        length = next_random() % 100 + 1
        message = random_message(length)
        decoded = decode_message(key, message)
        for b in decoded.encode():
            check = (check * 31 + b) % 1000000007
            if b == ord("a"):
                letters += 1
    print(f"2000 messages: checksum {check}, {letters} a's")


main()
