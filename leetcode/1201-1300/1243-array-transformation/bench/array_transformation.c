// LeetCode #1243: the benchmark, mirroring the Kāra file.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100
#define ARRAYS 5000

// The final array, written over `cur`; `next` is scratch of the same length.
static void transform_array(int64_t *cur, int64_t *next, int n) {
    for (;;) {
        memcpy(next, cur, n * sizeof(int64_t));
        for (int i = 1; i < n - 1; i++) {
            if (cur[i] < cur[i - 1] && cur[i] < cur[i + 1]) {
                next[i] += 1;
            } else if (cur[i] > cur[i - 1] && cur[i] > cur[i + 1]) {
                next[i] -= 1;
            }
        }
        if (memcmp(next, cur, n * sizeof(int64_t)) == 0) {
            return;
        }
        memcpy(cur, next, n * sizeof(int64_t));
    }
}

int main(void) {
    int64_t seed = 1243;
    int64_t *arrays = malloc(sizeof(int64_t) * N * ARRAYS);
    for (int a = 0; a < ARRAYS; a++) {
        for (int i = 0; i < N; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            arrays[a * N + i] = seed / 65536 % 100 + 1;
        }
    }
    int64_t cur[N], next[N];
    int64_t check = 0;
    for (int r = 0; r < 10; r++) {
        for (int a = 0; a < ARRAYS; a++) {
            memcpy(cur, arrays + a * N, sizeof cur);
            transform_array(cur, next, N);
            for (int i = 0; i < N; i++) {
                check = (check * 131 + cur[i]) % 1000000007;
            }
        }
    }
    printf("10 rounds of %d arrays of %d values: checksum %lld\n", ARRAYS, N, (long long)check);
    free(arrays);
    return 0;
}
