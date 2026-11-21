// LeetCode #2498: Frog Jump II -- C mirror of the benchmark (frog.kara):
// the same rows, passes and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2498;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t max_jump(const int64_t *stones, int64_t n) {
    int64_t cost = stones[1] - stones[0];
    for (int64_t i = 2; i < n; i++) {
        if (stones[i] - stones[i - 2] > cost) cost = stones[i] - stones[i - 2];
    }
    return cost;
}

int main(void) {
    const int64_t n = 100000, passes = 55;
    int64_t *rows[20];
    for (int r = 0; r < 20; r++) {
        rows[r] = malloc(n * sizeof(int64_t));
        rows[r][0] = 0;
        for (int64_t i = 1; i < n; i++) rows[r][i] = rows[r][i - 1] + next_random() % 10000 + 1;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int r = 0; r < 20; r++) {
            int64_t *stones = rows[r];
            int64_t at = check % (n - 2) + 1;
            int64_t was = stones[at];
            int64_t room = stones[at + 1] - stones[at - 1] - 1;
            if (room > 0) stones[at] = stones[at - 1] + 1 + (check + p) % room;
            check = (check * 31 + max_jump(stones, n) + p) % 1000000007;
            stones[at] = was;
        }
    }
    printf("%lld passes over 20 rows of 10^5: checksum %lld\n", (long long)passes, (long long)check);
    for (int r = 0; r < 20; r++) free(rows[r]);
    return 0;
}
