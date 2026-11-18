// LeetCode #2226: Maximum Candies Allocated to K Children -- the
// benchmark's C mirror of candies.kara: a binary search on the answer,
// x candies each possible when the piles give k shares of x.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t maximum_candies(const int64_t *candies, int64_t n, int64_t k) {
    int64_t low = 0, high = 0;
    for (int64_t i = 0; i < n; i++) if (candies[i] > high) high = candies[i];
    while (low < high) {
        int64_t x = (low + high + 1) / 2;
        int64_t shares = 0;
        for (int64_t i = 0; i < n; i++) shares += candies[i] / x;
        if (shares >= k) low = x;
        else high = x - 1;
    }
    return low;
}

static int64_t seed = 2226;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t *lists[4];
    for (int l = 0; l < 4; l++) {
        lists[l] = malloc(sizeof(int64_t) * N);
        for (int64_t i = 0; i < N; i++) lists[l][i] = wide_random() % 10000000 + 1;
    }
    const int64_t children[4] = {1000, 1000000, 1000000000, 100000000000LL};
    int64_t check = 0;
    for (int r = 0; r < 25; r++) {
        for (int l = 0; l < 4; l++) {
            // punch: one pile is drawn again before each answer
            int64_t at = wide_random() % N;
            lists[l][at] = wide_random() % 10000000 + 1;
            check = (check * 31 + maximum_candies(lists[l], N, children[l])) % 1000000007;
        }
    }
    printf("100 answers over 10^5 piles: checksum %lld\n", (long long)check);
    for (int l = 0; l < 4; l++) free(lists[l]);
    return 0;
}
