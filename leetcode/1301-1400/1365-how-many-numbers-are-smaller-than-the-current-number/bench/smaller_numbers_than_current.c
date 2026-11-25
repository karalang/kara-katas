// LeetCode #1365 bench -- C: the values counted and the counts summed, so
// below[v] holds how many values are less than v.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 500

static int32_t *smaller_numbers_than_current(const int32_t *nums, size_t n) {
    int32_t below[102] = {0};
    for (size_t i = 0; i < n; i++) below[nums[i] + 1] += 1;
    for (int v = 1; v < 102; v++) below[v] += below[v - 1];
    int32_t *out = malloc(sizeof *out * n);
    for (size_t i = 0; i < n; i++) out[i] = below[nums[i]];
    return out;
}

static int64_t seed = 1365;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 20 arrays of 500 values from 0 to 100, the constraints' most, built
    // once; then 2 * 10^5 rounds, each setting one value of one array, both
    // drawn from the checksum so far, and folding three of the answers
    // into the checksum
    static int32_t arrays[20][N];
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < N; i++) arrays[k][i] = (int32_t)(next_random() % 101);
    int64_t check = 0;
    for (int64_t r = 0; r < 200000; r++) {
        int64_t k = check % 20;
        arrays[k][(check / 20) % N] = (int32_t)((check / 10000) % 101);
        int32_t *got = smaller_numbers_than_current(arrays[k], N);
        check = (check * 31 + got[0] + (int64_t)got[check % N] * 7 + (int64_t)got[N - 1] * 13 + r) % 1000000007;
        free(got);
    }
    printf("200000 rounds over 20 arrays of 500 values: checksum %lld\n", (long long)check);
    return 0;
}
