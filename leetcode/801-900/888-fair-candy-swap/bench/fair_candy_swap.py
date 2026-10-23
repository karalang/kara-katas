# LeetCode #888 bench: a set of Bob's boxes, on 2000 cases of 5,000 to
# 10^4 boxes each, up to 10^5 candies a box. The same algorithm as
# fair_candy_swap.kara.


def fair_candy_swap(alice_sizes, bob_sizes):
    alice_total = sum(alice_sizes)
    bob_total = 0
    bob = set()
    for y in bob_sizes:
        bob_total += y
        bob.add(y)
    d = (bob_total - alice_total) // 2
    best = -1
    for x in alice_sizes:
        if x + d in bob and (best < 0 or x < best):
            best = x
    return [best, best + d]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(limit):
    hi = next_random()
    return (hi * 32768 + next_random()) % limit


# Alice's n boxes and Bob's m, of 1 to `most` candies, with a swap that
# evens the totals, built as in the Kāra harness (a box each can never be
# evened by a swap, so Bob then has two)
def case_boxes(n, m_drawn, most):
    m = 2 if n + m_drawn < 3 else m_drawn
    while True:
        alice = []
        alice_total = 0
        for _ in range(n):
            x = 1 + below(most)
            alice.append(x)
            alice_total += x
        bob = []
        for _ in range(m):
            bob.append(1 + below(most))
        i = below(n)
        j = below(m)
        y = 1 + below(most)
        bob[j] = y
        bob_total = sum(bob)
        short = alice_total + 2 * (y - alice[i]) - bob_total
        for k in range(m):
            if k != j and short != 0:
                step = min(max(short, 1 - bob[k]), most - bob[k])
                bob[k] += step
                short -= step
        for k in range(n):
            if k != i and short != 0:
                step = min(max(-short, 1 - alice[k]), most - alice[k])
                alice[k] += step
                short += step
        if short == 0 and y != alice[i]:
            return [alice, bob]


def main():
    global seed
    seed = 888
    gives = 0
    takes = 0
    check = 0
    for _ in range(2000):
        n = 5000 + below(5001)
        m = 5000 + below(5001)
        alice, bob = case_boxes(n, m, 100000)
        swap = fair_candy_swap(alice, bob)
        gives += swap[0]
        takes += swap[1]
        check = (check * 131 + swap[0] * 7 + swap[1]) % 1000000007
    print(f"2000 cases of 5000 to 10000 boxes: Alice gives {gives} candies, Bob {takes}, checksum {check}")


main()
