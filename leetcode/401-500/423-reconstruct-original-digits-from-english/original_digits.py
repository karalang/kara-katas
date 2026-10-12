# LeetCode #423: Reconstruct Original Digits from English -- mirror of
# original_digits.kara (unique letters).


def original_digits(s):
    letters = [0] * 26
    for ch in s:
        letters[ord(ch) - 97] += 1

    def at(c):
        return letters[ord(c) - 97]

    count = [0] * 10
    count[0] = at("z")
    count[2] = at("w")
    count[4] = at("u")
    count[6] = at("x")
    count[8] = at("g")
    count[3] = at("h") - count[8]
    count[5] = at("f") - count[4]
    count[7] = at("s") - count[6]
    count[1] = at("o") - count[0] - count[2] - count[4]
    count[9] = at("i") - count[5] - count[6] - count[8]
    return "".join(str(d) * count[d] for d in range(10))


seed = 423


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}": "{original_digits(s)}"')


show("owoztneoer")
show("fviefuro")
show("zero")
show("nine")
show("eightthree")
show("neninine")
show("seeevsixevisnsxn")
show("owtowtowt")
show("evunhtreoinexfestnvewerthsifieoonegi")
show("rofuhteonree")
names = "zero one two three four five six seven eight nine".split()
letters = 0
checksum = 0
for _ in range(2000):
    count = 1 + step() % 30
    pool = []
    for _ in range(count):
        digit = step() % 10
        pool.extend(names[digit])
    for i in range(len(pool)):
        j = i + step() % (len(pool) - i)
        pool[i], pool[j] = pool[j], pool[i]
    s = "".join(pool)
    answer = original_digits(s)
    letters += len(s)
    for ch in answer:
        checksum = (checksum * 31 + (ord(ch) - 47)) % 1000000007
print(f"2000 random strings, {letters} letters: checksum {checksum}")
