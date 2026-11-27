// LeetCode #1823: Find the Winner of the Circular Game -- the bench in C:
// the ★ arm over 200000 calls on circles of 250 to 499 friends, each
// circle's size and count drawn from the checksum so far.
#include <stdint.h>
#include <stdio.h>

static int64_t find_the_winner(int64_t n, int64_t k) {
    int64_t winner = 0;
    for (int64_t i = 2; i <= n; i++) winner = (winner + k) % i;
    return winner + 1;
}

int main(void) {
    int64_t check = 0;
    for (int64_t call = 0; call < 200000; call++) {
        int64_t n = 250 + (check + call) % 250;
        int64_t k = 1 + (check * 7 + call) % n;
        check = (check * 41 + find_the_winner(n, k)) % 1000000007;
    }
    printf("200000 calls: checksum %lld\n", (long long)check);
    return 0;
}
