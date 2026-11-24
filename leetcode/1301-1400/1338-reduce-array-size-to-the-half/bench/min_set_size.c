// LeetCode #1338 bench, C mirror of the Kāra bench: the ★ arm on 20 arrays
// of 10^5 values built once, then 30 passes, each setting one value of
// every array from the checksum so far, answering every array. C has no
// map, so the counts go in an open-addressing hash table.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_largest(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x;
    int64_t b = *(const int64_t *)y;
    return a < b ? 1 : (a > b ? -1 : 0);
}

static int32_t min_set_size(const int32_t *arr, int64_t n) {
    int64_t cap = 1;
    while (cap < 2 * n) {
        cap <<= 1;
    }
    int32_t *keys = calloc(cap, sizeof(int32_t));
    int64_t *counts = calloc(cap, sizeof(int64_t));
    int64_t distinct = 0;
    for (int64_t i = 0; i < n; i++) {
        uint64_t h = ((uint64_t)(uint32_t)arr[i] * 0x9E3779B97F4A7C15ULL) & (uint64_t)(cap - 1);
        while (keys[h] != 0 && keys[h] != arr[i]) {
            h = (h + 1) & (uint64_t)(cap - 1);
        }
        if (keys[h] == 0) {
            keys[h] = arr[i];
            distinct++;
        }
        counts[h]++;
    }
    int64_t *sizes = malloc(sizeof(int64_t) * distinct);
    int64_t k = 0;
    for (int64_t h = 0; h < cap; h++) {
        if (keys[h] != 0) {
            sizes[k++] = counts[h];
        }
    }
    qsort(sizes, k, sizeof(int64_t), by_largest);
    int64_t removed = 0;
    int32_t chosen = 0;
    for (int64_t i = 0; i < k; i++) {
        if (2 * removed >= n) {
            break;
        }
        removed += sizes[i];
        chosen++;
    }
    free(keys);
    free(counts);
    free(sizes);
    return chosen;
}

static int64_t seed = 1338;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int32_t *arrays[20];
    for (int t = 0; t < 20; t++) {
        int64_t top = t % 2 == 0 ? 100000 : 1000;
        arrays[t] = malloc(sizeof(int32_t) * n);
        for (int64_t i = 0; i < n; i++) {
            int64_t a = next_random();
            arrays[t][i] = (int32_t)(1 + (a * 32768 + next_random()) % top);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 30; pass++) {
        for (int t = 0; t < 20; t++) {
            int64_t at = check % n;
            arrays[t][at] = (int32_t)(1 + check / 3 % 1000);
            int32_t answer = min_set_size(arrays[t], n);
            check = (check * 31 + answer + pass) % 1000000007;
        }
    }
    printf("30 passes over 20 arrays of 10^5: checksum %lld\n", (long long)check);
    for (int t = 0; t < 20; t++) {
        free(arrays[t]);
    }
    return 0;
}
