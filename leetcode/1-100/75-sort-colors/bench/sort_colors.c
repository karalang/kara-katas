/*
 * Benchmark workload — Sort Colors (LeetCode #75), seq lane.
 * C single-threaded mirror of bench/sort_colors.kara. A batch of K=2000
 * independent Dutch National Flag sorts of n=59999 {0,1,2} arrays (length not a
 * multiple of 3, so the sorted result depends on the seed), each hashed, combined
 * through a plain associative sum. Single-threaded baseline; sort_colors_par.c is
 * the pthreads parallel comparator for Kara's auto-par. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define N 59999

/* Builds a fresh GROWING buffer per call (realloc-doubling from empty), matching
 * Kara's Vec.new()+push growth inside the function — NOT a malloc(N) upfront —
 * so the per-call allocation/growth cost is apples-to-apples (the #72 lesson). */
static int64_t sort_and_hash(int64_t seed) {
    int64_t *a = NULL;
    int64_t len = 0, cap = 0;
    for (int64_t j = 0; j < N; j++) {
        if (len == cap) {
            cap = cap ? cap * 2 : 1;
            a = (int64_t *)realloc(a, sizeof(int64_t) * (size_t)cap);
        }
        a[len++] = (j * 7 + seed) % 3;
    }

    int64_t low = 0, mid = 0, high = N - 1;
    while (mid <= high) {
        if (a[mid] == 0) {
            int64_t t = a[low]; a[low] = a[mid]; a[mid] = t;
            low++; mid++;
        } else if (a[mid] == 1) {
            mid++;
        } else {
            int64_t t = a[mid]; a[mid] = a[high]; a[high] = t;
            high--;
        }
    }

    int64_t acc = 0;
    for (int64_t j = 0; j < N; j++)
        acc = (acc * 131 + a[j]) % 1000000007;
    free(a);
    return acc;
}

int main(void) {
    const int64_t total = 2000;
    int64_t sum = 0;
    for (int64_t i = 0; i < total; i++)
        sum += sort_and_hash(i);
    printf("%lld\n", (long long)sum);
    return 0;
}
