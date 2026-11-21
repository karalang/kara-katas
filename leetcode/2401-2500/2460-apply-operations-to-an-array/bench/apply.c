// LeetCode #2460: Apply Operations to an Array -- the bench, the ★ arm in
// C: the operations in place, then the nonzero values moved forward by a
// write index and the rest filled with zeros. Each answer is made on a
// copy, as the other languages do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void apply_operations(int64_t *nums, int64_t n) {
    for (int64_t i = 0; i + 1 < n; i++) {
        if (nums[i] == nums[i + 1]) {
            nums[i] *= 2;
            nums[i + 1] = 0;
        }
    }
    int64_t k = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] != 0) nums[k++] = nums[i];
    }
    for (int64_t i = k; i < n; i++) nums[i] = 0;
}

static int64_t seed = 2460;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define ARRAYS 1000
#define N 2000

int main(void) {
    // 1000 arrays of 2000 values from 0 to 3 built once; then 24 passes,
    // each setting one value of every array from the checksum so far,
    // then answering every array on a copy and folding every value of
    // the answer, plus the pass, into the checksum
    int64_t *arrays = malloc(sizeof(int64_t) * ARRAYS * N);
    for (int64_t i = 0; i < ARRAYS * N; i++) arrays[i] = next_random() % 4;
    int64_t *copy = malloc(sizeof(int64_t) * N);
    int64_t check = 0;
    for (int64_t p = 0; p < 24; p++) {
        for (int64_t a = 0; a < ARRAYS; a++) {
            int64_t *row = arrays + a * N;
            row[(check + a) % N] = check % 4;
            memcpy(copy, row, sizeof(int64_t) * N);
            apply_operations(copy, N);
            for (int64_t i = 0; i < N; i++) check = (check * 31 + copy[i] + p) % 1000000007;
        }
    }
    free(copy);
    free(arrays);
    printf("24 passes over 1000 arrays of 2000: checksum %lld\n", (long long)check);
    return 0;
}
