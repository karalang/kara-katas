// Benchmark for #658: binary search for the window, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *find_closest_elements(const int64_t *arr, int64_t n, int64_t k, int64_t x) {
    int64_t low = 0, high = n - k;
    while (low < high) {
        int64_t middle = (low + high) / 2;
        if (x - arr[middle] > arr[middle + k] - x) low = middle + 1;
        else high = middle;
    }
    int64_t *out = malloc(k * sizeof *out);
    for (int64_t i = 0; i < k; i++) out[i] = arr[low + i];
    return out;
}

static int64_t seed = 658;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int64_t n = 1000000, queries = 1000000;
    int64_t *arr = malloc(n * sizeof *arr);
    for (int64_t i = 0; i < n; i++) {
        int64_t hi = next_random();
        int64_t lo = next_random();
        arr[i] = (hi * 32768 + lo) % 2000001 - 1000000;
    }
    qsort(arr, n, sizeof *arr, cmp);
    int64_t checksum = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t k = 1 + q % 64;
        int64_t hi = next_random();
        int64_t lo = next_random();
        int64_t x = (hi * 32768 + lo) % 2200001 - 1100000;
        int64_t *got = find_closest_elements(arr, n, k, x);
        checksum = (checksum * 31 + got[0] * 3 + got[k - 1] * 5 + k + 10000000) % 1000000007;
        free(got);
    }
    printf("%lld numbers, %lld queries: checksum %lld\n", (long long)n, (long long)queries, (long long)checksum);
    free(arr);
    return 0;
}
