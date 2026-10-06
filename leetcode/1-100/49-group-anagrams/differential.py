M = 18446744073709551557
MASK = (1 << 64) - 1
seed = 12345
def nxt():
    global seed
    seed = ((seed * 6364136223846793005) & MASK)
    seed = ((seed + 1442695040888963407) & MASK) % M
    return seed >> 33
words = []
for _ in range(4000):
    ln = nxt() % 5 + 1
    words.append(''.join(chr(ord('a') + nxt() % 4) for _ in range(ln)))
groups, order = {}, []
for i, w in enumerate(words):
    k = ''.join(sorted(w))
    if k not in groups:
        order.append(k); groups[k] = []
    groups[k].append(i)
check, biggest = 0, 0
for gi, k in enumerate(order):
    g = groups[k]; biggest = max(biggest, len(g))
    for idx in g:
        check = (check * 31 + idx * (gi + 1)) % 1000000007
print(f"{len(words)} words, {len(order)} groups, biggest {biggest}, checksum {check}")
