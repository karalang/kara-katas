// LeetCode #2161: Partition Array According to Given Pivot -- the
// benchmark's C mirror of pivot.kara: three passes into one output array.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2161;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static void pivot_array(const int64_t *nums, int64_t n, int64_t pivot, int64_t *out) {
    int64_t k = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] < pivot) {
            out[k++] = nums[i];
        }
    }
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == pivot) {
            out[k++] = nums[i];
        }
    }
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] > pivot) {
            out[k++] = nums[i];
        }
    }
}

static int64_t lists[4][N];

int main(void) {
    for (int l = 0; l < 4; l++) {
        for (int64_t i = 0; i < N; i++) {
            lists[l][i] = wide_random() % 2000001 - 1000000;
        }
    }
    int64_t *out = malloc(N * sizeof(int64_t));
    int64_t check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int l = 0; l < 4; l++) {
            int64_t at = wide_random() % N;
            lists[l][at] = wide_random() % 2000001 - 1000000;
            int64_t pivot = lists[l][wide_random() % N];
            pivot_array(lists[l], N, pivot, out);
            for (int64_t k = 0; k < 10; k++) {
                check = (check * 31 + out[k * 9999] + 1000001 + round) % 1000000007;
            }
        }
    }
    printf("100 solves: checksum %lld\n", (long long)check);
    free(out);
    return 0;
}
