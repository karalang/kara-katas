// LeetCode #1356 bench -- C: one sort keyed by the pair (the number of 1
// bits, the value), qsort with a comparison function.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_bits(const void *pa, const void *pb) {
    int32_t a = *(const int32_t *)pa, b = *(const int32_t *)pb;
    int ba = __builtin_popcount((unsigned)a), bb = __builtin_popcount((unsigned)b);
    if (ba != bb) return ba < bb ? -1 : 1;
    return (a > b) - (a < b);
}

static void sort_by_bits(const int32_t *arr, int32_t *out, int n) {
    memcpy(out, arr, n * sizeof(int32_t));
    qsort(out, n, sizeof(int32_t), by_bits);
}

static int64_t seed = 1356;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 20 arrays of 500 values from 0 to 10^4, the constraints' most, built
    // once; then 2 * 10^4 rounds, each setting one place of one array to a
    // value, all drawn from the checksum so far, sorting it, and folding
    // three values of the answer into the checksum
    static int32_t arrays[20][500];
    int32_t got[500];
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < 500; i++) arrays[k][i] = (int32_t)(next_random() % 10001);
    int64_t check = 0;
    for (int64_t r = 0; r < 20000; r++) {
        int64_t k = check % 20;
        arrays[k][(check / 20) % 500] = (int32_t)((check / 10000) % 10001);
        sort_by_bits(arrays[k], got, 500);
        check = (check * 31 + got[0] + (int64_t)got[check % 500] * 7 + (int64_t)got[499] * 13 + r) % 1000000007;
    }
    printf("20000 rounds over 20 arrays of 500 values: checksum %lld\n", (long long)check);
    return 0;
}
