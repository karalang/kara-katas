# LeetCode #1823: Find the Winner of the Circular Game -- the bench in
# Python: the ★ arm over 200000 calls on circles of 250 to 499 friends, each
# circle's size and count drawn from the checksum so far.


def find_the_winner(n, k):
    winner = 0
    for i in range(2, n + 1):
        winner = (winner + k) % i
    return winner + 1


check = 0
for call in range(200000):
    n = 250 + (check + call) % 250
    k = 1 + (check * 7 + call) % n
    check = (check * 41 + find_the_winner(n, k)) % 1000000007
print(f"200000 calls: checksum {check}")
