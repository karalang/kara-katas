# LeetCode #888: Fair Candy Swap -- Python mirror of the set-of-Bob's-boxes
# solution in fair_candy_swap.kara, with the same test harness.
#
# Swapping Alice's box x for Bob's box y evens the totals exactly when y
# - x is half the difference, d = (Bob's total - Alice's total) / 2. So
# put Bob's boxes in a set and look up x + d for each of Alice's. LeetCode
# accepts any such swap; this one returns the swap with Alice's smallest
# box, so that every arm prints the same. O(n + m).


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


# ---- test harness ----------------------------------------------------------


def show(alice_sizes, bob_sizes):
    swap = fair_candy_swap(alice_sizes, bob_sizes)
    a = ", ".join(str(x) for x in alice_sizes)
    b = ", ".join(str(y) for y in bob_sizes)
    print(f"alice = [{a}], bob = [{b}] -> [{swap[0]}, {swap[1]}]")


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
    show([1, 1], [2, 2])
    show([1, 2], [2, 3])
    show([2], [1, 3])
    show([1, 2, 5], [2, 4])
    show([6, 2], [9, 5])
    show([100000, 3], [99999, 2])
    show([3, 3, 3, 9], [3, 3, 3, 1, 4, 6])
    # small cases
    seed = 888
    gives = 0
    takes = 0
    for _ in range(3000):
        n = 1 + next_random() % 6
        m = 1 + next_random() % 6
        boxes = case_boxes(n, m, 12)
        swap = fair_candy_swap(boxes[0], boxes[1])
        gives += swap[0]
        takes += swap[1]
    print(f"3000 cases of up to 6 boxes of up to 12 candies: Alice gives {gives} candies, Bob {takes}")
    # LeetCode's sizes
    gives = 0
    takes = 0
    check = 0
    for _ in range(30):
        n = 1 + below(10000)
        m = 1 + below(10000)
        boxes = case_boxes(n, m, 100000)
        swap = fair_candy_swap(boxes[0], boxes[1])
        gives += swap[0]
        takes += swap[1]
        check = (check * 131 + swap[0] * 7 + swap[1]) % 1000000007
    print(f"30 cases of up to 10^4 boxes of up to 10^5 candies: Alice gives {gives} candies, Bob {takes}, checksum {check}")


main()
