// LeetCode #1122: Relative Sort Array -- the bench in C: the ★ arm over 4
// problems of 1000 values, each round swapping two values of each `arr1`
// and two of each `arr2` and sorting it again.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 1122;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// The answer written to `out`, which holds `n1` values.
static void relative_sort_array(const int32_t *arr1, int64_t n1, const int32_t *arr2, int64_t n2,
                                int32_t *out) {
    int64_t count[1001];
    memset(count, 0, sizeof count);
    for (int64_t i = 0; i < n1; i++) count[arr1[i]]++;
    int64_t at = 0;
    for (int64_t i = 0; i < n2; i++) {
        int32_t x = arr2[i];
        for (int64_t c = 0; c < count[x]; c++) out[at++] = x;
        count[x] = 0;
    }
    for (int32_t v = 0; v < 1001; v++)
        for (int64_t c = 0; c < count[v]; c++) out[at++] = v;
}

static int cmp(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static void swap(int32_t *a, int64_t i, int64_t j) {
    int32_t t = a[i];
    a[i] = a[j];
    a[j] = t;
}

int main(void) {
    const int64_t tops[4] = {1000, 500, 100, 10};
    int32_t ones[4][1000], twos[4][1001], out[1000];
    int64_t m[4];
    for (int j = 0; j < 4; j++) {
        for (int i = 0; i < 1000; i++) ones[j][i] = (int32_t)(next_random() % (tops[j] + 1));
        int32_t distinct[1000];
        memcpy(distinct, ones[j], sizeof distinct);
        qsort(distinct, 1000, sizeof(int32_t), cmp);
        int64_t d = 0;
        for (int i = 0; i < 1000; i++)
            if (d == 0 || distinct[d - 1] != distinct[i]) distinct[d++] = distinct[i];
        for (int64_t i = d - 1; i >= 1; i--) swap(distinct, i, next_random() % (i + 1));
        m[j] = (d + 1) / 2;
        memcpy(twos[j], distinct, m[j] * sizeof(int32_t));
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 5000; round++) {
        for (int j = 0; j < 4; j++) {
            swap(ones[j], round * 7919 % 1000, round * 104729 % 1000);
            swap(twos[j], round * 31 % m[j], round * 17 % m[j]);
            relative_sort_array(ones[j], 1000, twos[j], m[j], out);
            for (int i = 0; i < 1000; i++) check = (check * 31 + out[i]) % 1000000007;
        }
    }
    printf("5000 rounds over 4 problems of 1000 values: checksum %lld\n", (long long)check);
    return 0;
}
