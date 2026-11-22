// LeetCode #2826: Sorting Three Groups -- the bench's C mirror of the ★
// arm: a three-state table of the most numbers kept so far ending at a
// value at most v.

#include <stdio.h>
#include <stdlib.h>

static long long minimum_operations(const long long *nums, int n) {
    long long best[3] = {0, 0, 0};
    for (int i = 0; i < n; i++) {
        int v = (int)nums[i] - 1;
        best[v]++;
        for (int w = v + 1; w < 3; w++)
            if (best[v] > best[w]) best[w] = best[v];
    }
    return n - best[2];
}

static long long seed = 2826;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 200000, ROUNDS = 5 };
    long long (*cases)[100] = malloc(sizeof(long long[COUNT][100]));
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < 100; i++) cases[c][i] = next_random() % 3 + 1;
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            long long a = minimum_operations(cases[c], 100);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    printf("%d arrays of 100, %d rounds: %lld removals, checksum %lld\n", COUNT, ROUNDS, total, check);
    free(cases);
    return 0;
}
