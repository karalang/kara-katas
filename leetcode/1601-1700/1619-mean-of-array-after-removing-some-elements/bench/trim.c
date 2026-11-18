// LeetCode #1619: Mean of Array After Removing Some Elements -- the bench in
// C, mirroring trim.kara: sort a copy, then the mean of the middle 90%.
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp_i32(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static double trim_mean(const int32_t *arr, size_t n, int32_t *scratch) {
    memcpy(scratch, arr, n * sizeof(int32_t));
    qsort(scratch, n, sizeof(int32_t), cmp_i32);
    size_t k = n / 20;
    int64_t sum = 0;
    for (size_t i = k; i < n - k; i++) sum += scratch[i];
    return (double)sum / (double)(n - 2 * k);
}

static int64_t seed = 1619;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 20000, LEN = 1000 };
    int32_t *arrays = malloc(sizeof(int32_t) * COUNT * LEN);
    for (size_t i = 0; i < (size_t)COUNT * LEN; i++) {
        int64_t hi = next_random();
        int64_t lo = next_random();
        arrays[i] = (int32_t)((hi * 32768 + lo) % 100001);
    }
    int32_t *scratch = malloc(sizeof(int32_t) * LEN);
    int64_t check = 0;
    double total = 0.0;
    for (size_t a = 0; a < COUNT; a++) {
        double mean = trim_mean(arrays + a * LEN, LEN, scratch);
        total += mean;
        check = (check * 31 + (int64_t)round(mean * 100000.0) + 1) % 1000000007;
    }
    printf("20000 arrays of 1000 values: means sum to %.5f, checksum %lld\n", total, (long long)check);
    free(scratch);
    free(arrays);
    return 0;
}
