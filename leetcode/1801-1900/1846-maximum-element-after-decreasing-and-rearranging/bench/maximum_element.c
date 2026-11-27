// LeetCode #1846: Maximum Element After Decreasing and Rearranging -- the
// bench in C: the ★ arm over 200 calls on the first 50000 to 99999 of one
// list of 10^5 numbers from 1 to 60000, built once, each run's length drawn
// from the checksum so far. Each call is handed its own copy of its run,
// which the arm sorts.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t maximum_element_after_decrementing_and_rearranging(int64_t *arr, int64_t n) {
    qsort(arr, n, sizeof *arr, by_value);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        top = top + 1 < arr[i] ? top + 1 : arr[i];
    }
    return top;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1846;
    int64_t *base = malloc(100000 * sizeof *base);
    for (int64_t i = 0; i < 100000; i++) {
        int64_t hi = next_random(&seed);
        base[i] = 1 + (hi * 32768 + next_random(&seed)) % 60000;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        int64_t n = 50000 + (check + call) % 50000;
        int64_t *run = malloc(n * sizeof *run);
        memcpy(run, base, n * sizeof *run);
        check = (check * 31 + maximum_element_after_decrementing_and_rearranging(run, n)) % 1000000007;
        free(run);
    }
    printf("200 calls: checksum %lld\n", (long long)check);
    free(base);
    return 0;
}
