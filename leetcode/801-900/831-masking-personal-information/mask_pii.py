# LeetCode 831 — Masking Personal Information, by the rules.
#
# Mirrors mask_pii.kara: an email keeps its name's first and last letter,
# lowered, around five `*`, and its domain lowered; a phone number shows
# its last four digits and masks the country code.

def mask_pii(s):
    at = s.find("@")
    if at >= 0:
        lower = s.lower()
        return f"{lower[0]}*****{lower[at - 1:]}"
    digits = "".join(c for c in s if c.isdigit())
    n = len(digits)
    local = f"***-***-{digits[n - 4:]}"
    return local if n == 10 else f"+{'*' * (n - 10)}-{local}"

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def show(s):
    print(f'"{s}" -> "{mask_pii(s)}"')

def random_email():
    s = ""
    for part in range(3):
        length = 2 + next_random() % 9
        for _ in range(length):
            r = next_random() % 52
            s += chr(ord('a') + r) if r < 26 else chr(ord('A') + r - 26)
        if part == 0:
            s += "@"
        elif part == 1:
            s += "."
    return s

def random_phone():
    separators = ['+', '-', '(', ')', ' ']
    digits = 10 + next_random() % 4
    s = ""
    for _ in range(digits):
        if next_random() % 3 == 0:
            s += separators[next_random() % 5]
        s += chr(ord('0') + next_random() % 10)
    return s

for s in ["LeetCode@LeetCode.com", "AB@qq.com", "1(234)567-890", "ab@b.c", "ZzZ@QQ.COM",
          "1234567890", "+1 (234) 567-8901", "+12 345 678 9012", "+(123)-456-789-0123"]:
    show(s)
seed = 831
total = 0
check = 0
for i in range(400):
    s = random_email() if i % 2 == 0 else random_phone()
    m = mask_pii(s)
    total += len(m)
    for b in m.encode():
        check = (check * 131 + b) % 1000000007
print(f"400 random strings: {total} characters, checksum {check}")
