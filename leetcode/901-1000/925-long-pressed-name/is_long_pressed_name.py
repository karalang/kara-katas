# LeetCode #925: Long Pressed Name -- two pointers (Python mirror).


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


def show(name, typed):
    print(f'"{name}", "{typed}": {str(is_long_pressed_name(name, typed)).lower()}')


def random_case(n, letters):
    name = [chr(ord("a") + next_random() % letters) for _ in range(n)]
    typed = []
    for c in name:
        extra = 1 + next_random() % 3 if next_random() % 4 == 0 else 0
        typed.extend([c] * (1 + extra))
    how = next_random() % 6
    at = next_random() % len(typed)
    letter = chr(ord("a") + next_random() % letters)
    if how == 0:
        del typed[at]
    elif how == 1:
        typed.insert(at, letter)
    elif how == 2:
        typed[at] = letter
    if not typed:
        typed.append(letter)
    return "".join(name), "".join(typed)


def main():
    show("alex", "aaleex")
    show("saeed", "ssaaedd")
    show("laiden", "laiden")
    show("a", "aaaa")
    show("aab", "ab")
    show("abc", "abcd")
    show("a", "b")
    show("leelee", "lleeelee")
    show("alex", "alexxr")
    show("vtkgn", "vttkgnn")
    show("abc", "ab")
    yes = 0
    check = 0
    for r in range(300):
        n = 1 + next_random() % 200
        letters = 2 if r % 3 == 0 else 3 if r % 3 == 1 else 26
        name, typed = random_case(n, letters)
        bit = 1 if is_long_pressed_name(name, typed) else 0
        yes += bit
        check = (check * 1000003 + bit * (r + 1)) % 1000000007
    print(f"300 random names: {yes} long pressed, checksum {check}")
    z = "z" * 1000
    abab = "".join("a" if i % 2 == 0 else "b" for i in range(1000))
    h = "".join(chr(ord("a") + i % 26) for i in range(500))
    t = "".join(c + c for c in h)
    f = lambda x, y: str(is_long_pressed_name(x, y)).lower()
    print(f"1000 letters: z against z {f(z, z)}, ab against ab {f(abab, abab)}, each typed twice {f(h, t)}, twice against once {f(t, h)}")


main()
