// LeetCode 801 — Minimum Swaps To Make Sequences Increasing: the bench,
// in C. Mirrors min_swap.kara: two states, left alone and swapped.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t min_swap(const int64_t *nums1, const int64_t *nums2, int64_t n) {
    int64_t keep = 0, swap = 1;
    for (int64_t i = 1; i < n; i++) {
        int same = nums1[i - 1] < nums1[i] && nums2[i - 1] < nums2[i];
        int cross = nums1[i - 1] < nums2[i] && nums2[i - 1] < nums1[i];
        int64_t next_keep = n + 1, next_swap = n + 1;
        if (same) {
            next_keep = keep;
            next_swap = swap + 1;
        }
        if (cross) {
            next_keep = min64(next_keep, swap);
            next_swap = min64(next_swap, keep + 1);
        }
        keep = next_keep;
        swap = next_swap;
    }
    return min64(keep, swap);
}

static int64_t seed = 801;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *as[16], *bs[16];
    for (int p = 0; p < 16; p++) {
        as[p] = malloc(n * sizeof(int64_t));
        bs[p] = malloc(n * sizeof(int64_t));
        int64_t x = 0, y = 0;
        for (int64_t i = 0; i < n; i++) {
            x += 1 + next_random() % 2;
            y += 1 + next_random() % 2;
            if (next_random() % 2 == 0) {
                as[p][i] = x;
                bs[p][i] = y;
            } else {
                as[p][i] = y;
                bs[p][i] = x;
            }
        }
    }
    const int64_t rounds = 2000;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = min_swap(as[r % 16], bs[r % 16], n);
        total += k;
        check = (check * 131 + k) % 1000000007;
    }
    printf("%lld rounds of %lld places: %lld swaps in all, checksum %lld\n", (long long)rounds, (long long)n,
           (long long)total, (long long)check);
    return 0;
}
