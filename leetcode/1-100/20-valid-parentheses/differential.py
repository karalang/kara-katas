# Mirror of differential.kara: stack check vs pair-deletion on 3000 LCG bracket strings.
def by_stack(s):
    want = []
    pair = {'(': ')', '[': ']', '{': '}'}
    for c in s:
        if c in pair:
            want.append(pair[c])
        elif not want or want.pop() != c:
            return False
    return not want

def by_deletion(s):
    cur = s
    while True:
        nxt = cur.replace("()", "").replace("[]", "").replace("{}", "")
        if len(nxt) == len(cur):
            return nxt == ""
        cur = nxt

alphabet = ['(', ')', '[', ']', '{', '}']
seed, valid, fails, checksum = 777, 0, 0, 0
for t in range(3000):
    seed = (seed * 1103515245 + 12345) % 2147483648
    n = 2 * (seed % 9)
    s, opens = [], []
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) % 2147483648
        r = (seed // 8) % 10
        if r < 6 and len(opens) < 8:
            k = r % 3
            opens.append(k)
            s.append(alphabet[2 * k])
        elif opens and r < 9:
            k = opens.pop()
            s.append(alphabet[2 * k + 1])
        else:
            s.append(alphabet[r % 6])
    s = ''.join(s)
    a, b = by_stack(s), by_deletion(s)
    if a != b:
        fails += 1
        print(f"mismatch {t}: {s}")
    if a:
        valid += 1
    checksum = (checksum * 3 + (1 if a else 0) + len(s)) % 1000000007
print(f"3000 strings, {valid} valid, failures {fails}, checksum {checksum}")
