# LeetCode #925: Long Pressed Name -- bench: two pointers.
# Mirrors is_long_pressed_name.kara.


def is_long_pressed_name(name, typed):
    a = name.encode()
    b = typed.encode()
    i = 0
    for j in range(len(b)):
        if i < len(a) and a[i] == b[j]:
            i += 1
        elif j > 0 and b[j] == b[j - 1]:
            continue
        else:
            return False
    return i == len(a)


seed = 925


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count = 150, 1000
    # count names of 400 letters from "abc", each typed with about one key
    # in four held down for up to three more presses, and every third one
    # mistyped once
    names = []
    typings = []
    for p in range(count):
        name = []
        typed = []
        for _ in range(400):
            c = chr(ord("a") + next_random() % 3)
            name.append(c)
            extra = 1 + next_random() % 3 if next_random() % 4 == 0 else 0
            typed.extend([c] * (1 + extra))
        if p % 3 == 0:
            at = next_random() % len(typed)
            typed[at] = chr(ord("a") + next_random() % 3)
        names.append("".join(name))
        typings.append("".join(typed))
    yes = 0
    check = 0
    for r in range(rounds):
        # each round visits every pair, starting from a different one
        for i in range(count):
            p = (r + i) % count
            if is_long_pressed_name(names[p], typings[p]):
                yes += 1
                check = (check * 1000003 + p + 1) % 1000000007
    print(f"{rounds} rounds over {count} names of 400 letters: {yes} long pressed, checksum {check}")


main()
