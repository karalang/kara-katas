# benchmark's Python mirror of archery.kara (LeetCode #2212, the ★ arm):
# all 2^12 sets of sections tried as bit masks, Bob paying alice[k] + 1
# arrows for each, the best he can afford kept, and the arrows left over
# put in section 0.


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


seed = 2212


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    contests = []
    for _ in range(3000):
        # up to 10^5 arrows, Alice's shot into 12 sections in random shares
        n = next_random() * 4 % 100000 + 1
        alice = [0] * 12
        left = n
        for k in range(11):
            take = next_random() % (left // 4 + 1)
            alice[k] = take
            left -= take
        alice[11] = left
        contests.append((n, alice))
    check = 0
    for n, alice in contests:
        bob = maximum_bob_points(n, alice)
        for k in range(12):
            check = (check * 31 + bob[k]) % 1000000007
    print(f"3000 contests: checksum {check}")


main()
