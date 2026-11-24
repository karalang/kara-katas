// LeetCode #1331 bench, C mirror of the Kāra bench: the ★ arm (the values
// sorted with `qsort`, their repeats removed, and each value's rank found
// by binary search) on 20 arrays of 10^5 values, the constraints' longest,
// each from 1 to 10^9 or from a narrower spread with many repeats, built
// once. Then 15 passes, each setting one value of every array from the
// checksum so far, answering it and folding two of its ranks plus the pass
// into the checksum. Each call takes a fresh copy to sort and a fresh
// answer, as the Kāra arm clones and collects.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp_i32(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static int32_t *array_rank_transform(const int32_t *arr, int64_t n) {
    int32_t *distinct = malloc((size_t)n * sizeof(int32_t));
    memcpy(distinct, arr, (size_t)n * sizeof(int32_t));
    qsort(distinct, (size_t)n, sizeof(int32_t), cmp_i32);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++)
        if (m == 0 || distinct[m - 1] != distinct[i]) distinct[m++] = distinct[i];
    int32_t *ranks = malloc((size_t)n * sizeof(int32_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t lo = 0, hi = m;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (distinct[mid] < arr[i]) lo = mid + 1;
            else hi = mid;
        }
        ranks[i] = (int32_t)(lo + 1);
    }
    free(distinct);
    return ranks;
}

static int64_t seed = 1331;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    static int32_t arrays[20][100000];
    for (int t = 0; t < 20; t++) {
        int64_t spread = t % 2 == 0 ? 1000000000 : 1000;
        for (int64_t i = 0; i < n; i++) {
            int64_t a = next_random();
            int64_t b = next_random();
            arrays[t][i] = (int32_t)((a * 61036 + b) % spread + 1);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 15; pass++) {
        for (int t = 0; t < 20; t++) {
            int64_t at = check % n;
            arrays[t][at] = (int32_t)(check / 7 % 1000000000 + 1);
            int32_t *ranks = array_rank_transform(arrays[t], n);
            check = (check * 31 + ranks[at] + ranks[n - 1] + pass) % 1000000007;
            free(ranks);
        }
    }
    printf("15 passes over 20 arrays of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
