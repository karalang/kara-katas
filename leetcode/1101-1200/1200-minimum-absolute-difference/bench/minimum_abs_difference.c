// LeetCode #1200 bench: the ★ arm in C, over the same 20 arrays of 10^5
// values and 10 rounds as the Kāra bench; each call copies its array and
// sorts the copy with `qsort`.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static int ascending(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// The pairs go to `pairs` as (smaller, larger); returns how many.
static int64_t minimum_abs_difference(const int64_t *src, int64_t n, int64_t *arr, int64_t *pairs) {
    memcpy(arr, src, n * sizeof(int64_t));
    qsort(arr, n, sizeof(int64_t), ascending);
    int64_t least = INT64_MAX;
    for (int64_t i = 1; i < n; i++) {
        if (arr[i] - arr[i - 1] < least) least = arr[i] - arr[i - 1];
    }
    int64_t count = 0;
    for (int64_t i = 1; i < n; i++) {
        if (arr[i] - arr[i - 1] == least) {
            pairs[2 * count] = arr[i - 1];
            pairs[2 * count + 1] = arr[i];
            count++;
        }
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t spans[3] = {1000000, 100000, 60000};
    int64_t seed = 1200;
    int64_t *arrays = malloc(20 * N * sizeof(int64_t));
    for (int k = 0; k < 20; k++) {
        int64_t span = spans[k % 3];
        char *taken = calloc(2 * span + 1, 1);
        int64_t len = 0;
        while (len < N) {
            int64_t a = next_random(&seed);
            int64_t b = next_random(&seed);
            int64_t v = (a * 32768 + b) % (2 * span + 1) - span;
            if (!taken[v + span]) {
                taken[v + span] = 1;
                arrays[k * N + len++] = v;
            }
        }
        free(taken);
    }
    int64_t *arr = malloc(N * sizeof(int64_t));
    int64_t *pairs = malloc(2 * N * sizeof(int64_t));
    int64_t check = 0;
    for (int r = 0; r < 10; r++) {
        for (int k = 0; k < 20; k++) {
            int64_t count = minimum_abs_difference(arrays + k * N, N, arr, pairs);
            check = (check * 131 + count) % 1000000007;
            for (int64_t p = 0; p < count; p++) {
                check = (check * 131 + pairs[2 * p] + pairs[2 * p + 1] + 2000000) % 1000000007;
            }
        }
    }
    printf("10 rounds of 20 arrays of 100000 values: checksum %lld\n", (long long)check);
    free(pairs);
    free(arr);
    free(arrays);
    return 0;
}
