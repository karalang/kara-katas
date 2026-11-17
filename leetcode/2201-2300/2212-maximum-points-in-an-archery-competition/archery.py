# Python mirror of archery.kara (LeetCode #2212, the ★ arm): all 2^12 sets
# of sections tried as bit masks, Bob paying alice[k] + 1 arrows for each,
# the best he can afford kept, and the arrows left over put in section 0.


def maximum_bob_points(num_arrows, alice_arrows):
    best_mask = 0
    best_points = -1
    for mask in range(4096):
        cost = points = 0
        for k in range(12):
            if mask >> k & 1 == 1:
                cost += alice_arrows[k] + 1
                points += k
        if cost <= num_arrows and points > best_points:
            best_points = points
            best_mask = mask
    bob = [0] * 12
    left = num_arrows
    for k in range(12):
        if best_mask >> k & 1 == 1:
            bob[k] = alice_arrows[k] + 1
            left -= bob[k]
    bob[0] += left
    return bob


# ---- test harness ---------------------------------------------------------


def score(num_arrows, alice, bob):
    if len(bob) != 12 or any(b < 0 for b in bob) or sum(bob) != num_arrows:
        return -1
    return sum(k for k in range(12) if bob[k] > alice[k])


seed = 2212


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_alice(n):
    alice = [0] * 12
    for _ in range(n):
        alice[next_random() % 12] += 1
    return alice


def show(num_arrows, alice):
    bob = maximum_bob_points(num_arrows, alice)
    print(f"{num_arrows} vs [{', '.join(map(str, alice))}] -> {score(num_arrows, alice, bob)}")


def main():
    # LeetCode's two examples, then four more: one arrow, Alice's arrows
    # all in section 11, all in section 0, and spread one to a section
    show(9, [1, 1, 0, 1, 0, 0, 2, 1, 0, 1, 2, 0])
    show(3, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2])
    show(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    show(5, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5])
    show(7, [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    show(12, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    # 3000 random contests of 1 to 30 arrows, then of 1 to 10^5
    check = 0
    for c in range(3000):
        n = next_random() % 30 + 1 if c < 2000 else next_random() * 4 % 100000 + 1
        alice = random_alice(n)
        bob = maximum_bob_points(n, alice)
        check = (check * 31 + score(n, alice, bob)) % 1000000007
    print(f"3000 contests: checksum {check}")
    # the constraints' largest: 10^5 arrows, Alice's spread evenly, and
    # all but 11 in section 11
    even = [8333] * 12
    even[0] += 4
    heavy = [1] * 12
    heavy[11] = 100000 - 11
    print(f"10^5 even -> {score(100000, even, maximum_bob_points(100000, even))}, 10^5 heavy -> {score(100000, heavy, maximum_bob_points(100000, heavy))}")


main()
