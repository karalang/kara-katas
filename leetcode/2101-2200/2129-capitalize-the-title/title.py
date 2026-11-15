# LeetCode #2129: Capitalize the Title -- the mirror of title.kara: each
# word lowered, and a word of three letters or more given a capital.


def capitalize_title(title):
    words = []
    for w in title.split(" "):
        lower = w.lower()
        words.append(lower if len(lower) <= 2 else lower[:1].upper() + lower[1:])
    return " ".join(words)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(title):
    print(f'"{title}" -> "{capitalize_title(title)}"')


def main():
    show("capiTalIze tHe titLe")
    show("First leTTeR of EACH Word")
    show("i lOve leetcode")
    show("A")
    show("OF")
    show("thE")
    show("a Bc DEF ghIj klmnO")
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seed = [2129]
    capitals = 0
    check = 0
    for _ in range(3000):
        words = next_random(seed) % 8 + 1
        title = ""
        for w in range(words):
            if w > 0:
                title += " "
            n = next_random(seed) % 6 + 1
            for _ in range(n):
                k = next_random(seed) % 52
                title += letters[k]
        for b in capitalize_title(title).encode():
            if 65 <= b <= 90:
                capitals += 1
            check = (check * 31 + b) % 1000000007
    print(f"3000 titles: {capitals} capitals, checksum {check}")
    a = capitalize_title(" ".join(["X"] * 50))
    b = capitalize_title(" ".join(["xY"] * 33))
    c = capitalize_title(" ".join(["xYz"] * 25))
    print(f'{len(a)}, {len(b)} and {len(c)} long: "{a[:5]} ..", "{b[:8]} ..", "{c[:11]} .."')


main()
