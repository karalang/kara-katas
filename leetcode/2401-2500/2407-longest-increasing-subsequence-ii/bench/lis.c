// LeetCode #2407: Longest Increasing Subsequence II -- the bench, the ★
// arm in C: a bottom-up segment tree over the values, the longest ending
// at x one more than the tree's maximum over x - k to x - 1.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2407;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t length_of_lis(const int64_t *nums, int64_t n, int64_t k) {
    int64_t top = nums[0];
    for (int64_t i = 1; i < n; i++) top = max64(top, nums[i]);
    int64_t size = 1;
    while (size <= top) size *= 2;
    int64_t *tree = calloc(2 * size, sizeof *tree);
    int64_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        int64_t lo = max64(x - k, 0) + size, hi = x - 1 + size + 1, longest = 0;
        while (lo < hi) {
            if (lo % 2 == 1) longest = max64(longest, tree[lo++]);
            if (hi % 2 == 1) longest = max64(longest, tree[--hi]);
            lo /= 2;
            hi /= 2;
        }
        int64_t at = x + size;
        tree[at] = max64(tree[at], longest + 1);
        best = max64(best, longest + 1);
        for (at /= 2; at > 0; at /= 2) tree[at] = max64(tree[2 * at], tree[2 * at + 1]);
    }
    free(tree);
    return best;
}

int main(void) {
    static int64_t arrays[5][N];
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < N; j++) arrays[i][j] = 1 + (next_random() * 32768 + next_random()) % 100000;
    int64_t check = 0;
    for (int64_t p = 0; p < 4; p++) {
        int64_t k = 1;
        for (int i = 0; i < 5; i++, k *= 10) check = (check * 31 + length_of_lis(arrays[i], N, k) + p) % 1000000007;
    }
    printf("4 passes over 5 arrays of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
