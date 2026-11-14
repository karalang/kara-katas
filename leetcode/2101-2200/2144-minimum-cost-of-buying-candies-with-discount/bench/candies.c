// LeetCode #2144: Minimum Cost of Buying Candies With Discount -- the
// benchmark, the same algorithm as candies.kara: a sort dearest first (a
// merge sort, stable like Kāra's `sort_by`), every third free.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100
#define B 1000

static void merge_sort_desc(int64_t *a, int64_t *tmp, int64_t n) {
    if (n < 2) return;
    int64_t h = n / 2;
    merge_sort_desc(a, tmp, h);
    merge_sort_desc(a + h, tmp, n - h);
    int64_t i = 0, j = h, k = 0;
    while (i < h && j < n) tmp[k++] = a[j] > a[i] ? a[j++] : a[i++];
    while (i < h) tmp[k++] = a[i++];
    while (j < n) tmp[k++] = a[j++];
    memcpy(a, tmp, n * sizeof(int64_t));
}

static int64_t minimum_cost(const int64_t *cost, int64_t n) {
    int64_t dearest_first[N], tmp[N];
    memcpy(dearest_first, cost, n * sizeof(int64_t));
    merge_sort_desc(dearest_first, tmp, n);
    int64_t paid = 0;
    for (int64_t i = 0; i < n; i++)
        if (i % 3 != 2) paid += dearest_first[i];
    return paid;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2144;
    int64_t (*baskets)[N] = malloc(sizeof(int64_t[B][N]));
    for (int b = 0; b < B; b++)
        for (int i = 0; i < N; i++) baskets[b][i] = next_random(&seed) % 100 + 1;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int b = 0; b < B; b++) {
            int64_t at = next_random(&seed) % N;
            baskets[b][at] = next_random(&seed) % 100 + 1;
            int64_t paid = minimum_cost(baskets[b], N);
            total += paid;
            check = (check * 31 + paid + round) % 1000000007;
        }
    }
    printf("100000 solves: %lld paid in all, checksum %lld\n", (long long)total, (long long)check);
    free(baskets);
    return 0;
}
