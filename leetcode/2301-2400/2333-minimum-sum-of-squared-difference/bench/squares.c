// LeetCode #2333: Minimum Sum of Squared Difference -- the bench, the ★
// arm in C: the gaps counted by size, the largest dropped a level at a
// time while the moves cover them, and the moves left taking that many
// of the rest one lower.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PAIRS 20000
#define TOP 100001

static int64_t min_sum_square_diff(const int64_t *nums1, const int64_t *nums2, int n, int64_t k1, int64_t k2) {
    int64_t *count = calloc(TOP, sizeof(int64_t));
    int64_t top = 0;
    for (int i = 0; i < n; i++) {
        int64_t gap = llabs(nums1[i] - nums2[i]);
        count[gap] += 1;
        if (gap > top) top = gap;
    }
    int64_t moves = k1 + k2;
    int64_t level = top;
    while (level > 0 && moves >= count[level]) {
        moves -= count[level];
        count[level - 1] += count[level];
        count[level] = 0;
        level -= 1;
    }
    if (level > 0) {
        count[level] -= moves;
        count[level - 1] += moves;
    }
    int64_t total = 0;
    for (int64_t gap = 1; gap <= level; gap++) total += count[gap] * gap * gap;
    free(count);
    return total;
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    static int64_t nums1[10][PAIRS], nums2[10][PAIRS];
    for (int64_t c = 0; c < 10; c++) {
        for (int64_t i = 0; i < PAIRS; i++) {
            nums1[c][i] = scrambled(c * 40000 + i) % 100001;
            nums2[c][i] = scrambled(c * 40000 + 20000 + i) % 100001;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++) {
        for (int64_t c = 0; c < 10; c++) {
            int64_t k1 = (10 * c + p) * 3000000 % 400000000;
            int64_t k2 = (7 * p + c) * 5000000 % 300000000;
            check = (check * 31 + min_sum_square_diff(nums1[c], nums2[c], PAIRS, k1, k2)) % 1000000007;
        }
    }
    printf("10 passes over 10 cases of 2*10^4 pairs: checksum %lld\n", (long long)check);
    return 0;
}
