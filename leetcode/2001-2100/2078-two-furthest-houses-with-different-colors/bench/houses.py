# LeetCode #2078: Two Furthest Houses With Different Colors -- Python
# mirror of the ★ arm's benchmark (houses.kara): 20000 streets of 100
# houses, 1000 rounds each recoloring one house of every street and
# answering every street that still has two colors with a scan in from
# each end.


def max_distance(colors):
    n = len(colors)
    j = n - 1
    while colors[j] == colors[0]:
        j -= 1
    i = 0
    while colors[i] == colors[n - 1]:
        i += 1
    return max(j, n - 1 - i)


seed = 2078


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


streets = []
for _ in range(20000):
    colors = [0] * 100
    a = next_random() % 100
    colors[a] = next_random() % 3 + 1
    b = next_random() % 100
    colors[b] = next_random() % 3 + 1
    streets.append(colors)
answered = total = check = 0
for _ in range(1000):
    for colors in streets:
        k = next_random() % 100
        colors[k] = 0 if next_random() % 2 == 0 else next_random() % 3 + 1
        if any(c != colors[0] for c in colors):
            a = max_distance(colors)
            answered += 1
            total += a
            check = (check * 31 + a) % 1000000007
print(f"{answered} answers: sum {total}, checksum {check}")
