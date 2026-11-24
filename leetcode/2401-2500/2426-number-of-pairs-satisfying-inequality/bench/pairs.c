// LeetCode #2426: Number of Pairs Satisfying Inequality -- the bench, the
// ★ arm: with `a[i] = nums1[i] - nums2[i]`, a merge sort counting the
// pairs `i < j` with `a[i] <= a[j] + diff`. Each merge fills a buffer
// grown by doubling, as the other languages' growable lists do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_pairs(int64_t *a, int64_t lo, int64_t hi, int64_t diff) {
    if (hi - lo < 2) return 0;
    int64_t mid = (lo + hi) / 2;
    int64_t count = count_pairs(a, lo, mid, diff) + count_pairs(a, mid, hi, diff);
    int64_t p = lo;
    for (int64_t j = mid; j < hi; j++) {
        while (p < mid && a[p] <= a[j] + diff) p++;
        count += p - lo;
    }
    int64_t cap = 4, len = 0;
    int64_t *merged = malloc((size_t)cap * sizeof(int64_t));
    int64_t i = lo, j = mid;
    while (i < mid || j < hi) {
        if (len == cap) {
            cap *= 2;
            merged = realloc(merged, (size_t)cap * sizeof(int64_t));
        }
        if (j == hi || (i < mid && a[i] <= a[j])) merged[len++] = a[i++];
        else merged[len++] = a[j++];
    }
    for (int64_t k = 0; k < len; k++) a[lo + k] = merged[k];
    free(merged);
    return count;
}

static int64_t number_of_pairs(const int64_t *nums1, const int64_t *nums2, int64_t n, int64_t diff) {
    int64_t *a = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) a[i] = nums1[i] - nums2[i];
    int64_t count = count_pairs(a, 0, n, diff);
    free(a);
    return count;
}

static int64_t seed = 2426;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *firsts[10], *seconds[10];
    for (int c = 0; c < 10; c++) {
        firsts[c] = malloc((size_t)n * sizeof(int64_t));
        seconds[c] = malloc((size_t)n * sizeof(int64_t));
        for (int64_t k = 0; k < n; k++) {
            firsts[c][k] = next_random() % 20001 - 10000;
            seconds[c][k] = next_random() % 20001 - 10000;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 4; p++) {
        for (int64_t c = 0; c < 10; c++) {
            int64_t diff = 2000 * c - 10000 + p - 2;
            check = (check * 31 + number_of_pairs(firsts[c], seconds[c], n, diff) + p) % 1000000007;
        }
    }
    printf("4 passes over 10 cases of 10^5 values: checksum %lld\n", (long long)check);
    for (int c = 0; c < 10; c++) {
        free(firsts[c]);
        free(seconds[c]);
    }
    return 0;
}
