// LeetCode #2164: Sort Even and Odd Indices Independently -- the
// benchmark's C mirror of parity.kara: each parity copied out and sorted
// by qsort, rising and falling.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int rising(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int falling(const void *a, const void *b) { return rising(b, a); }

static void sort_even_odd(const int64_t *nums, int64_t len, int64_t *out) {
    int64_t even[64], odd[64], ne = 0, no = 0;
    for (int64_t i = 0; i < len; i++) {
        if (i % 2 == 0) even[ne++] = nums[i];
        else odd[no++] = nums[i];
    }
    qsort(even, (size_t)ne, sizeof(int64_t), rising);
    qsort(odd, (size_t)no, sizeof(int64_t), falling);
    for (int64_t i = 0; i < len; i++) out[i] = i % 2 == 0 ? even[i / 2] : odd[i / 2];
}

static int64_t seed = 2164;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t lists[1000][100];
    int64_t copy[100], out[100];
    for (int k = 0; k < 1000; k++)
        for (int i = 0; i < 100; i++) lists[k][i] = next_random() % 100 + 1;
    int64_t check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int64_t k = 0; k < 1000; k++) {
            int64_t at = next_random() % 100;
            lists[k][at] = next_random() % 100 + 1;
            memcpy(copy, lists[k], sizeof copy);
            sort_even_odd(copy, 100, out);
            check = (check * 31 + out[round % 100] + out[(k * 7) % 100]) % 1000000007;
        }
    }
    printf("200000 solves: checksum %lld\n", (long long)check);
    return 0;
}
