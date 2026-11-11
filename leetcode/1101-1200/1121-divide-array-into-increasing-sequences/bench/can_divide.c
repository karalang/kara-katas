// LeetCode #1121: Divide Array Into Increasing Sequences -- the bench in
// C: the ★ arm over 4 sorted arrays of 100000 values, each round copying
// one value over its neighbour and answering for a new `k`.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 1121;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static bool can_divide_into_subsequences(const int32_t *nums, int64_t n, int32_t k) {
    int64_t longest = 0, run = 0;
    for (int64_t i = 0; i < n; i++) {
        run = (i > 0 && nums[i] == nums[i - 1]) ? run + 1 : 1;
        if (run > longest) longest = run;
    }
    return longest * k <= n;
}

static int cmp(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    enum { N = 100000, ARRAYS = 4 };
    const int64_t tops[ARRAYS] = {2000, 1000, 500, 200};
    int32_t *arrays[ARRAYS];
    for (int j = 0; j < ARRAYS; j++) {
        arrays[j] = malloc(sizeof(int32_t) * N);
        for (int64_t i = 0; i < N; i++) arrays[j][i] = (int32_t)(next_random() % tops[j] + 1);
        qsort(arrays[j], N, sizeof(int32_t), cmp);
    }
    int64_t yes = 0, check = 0;
    for (int64_t round = 0; round < 250; round++) {
        for (int64_t j = 0; j < ARRAYS; j++) {
            int64_t at = (round * 7919 + j * 104729) % (N - 2) + 1;
            arrays[j][at] = round % 2 == 0 ? arrays[j][at + 1] : arrays[j][at - 1];
            int32_t k = (int32_t)((round * 13 + j * 7) % 2000 + 1);
            bool r = can_divide_into_subsequences(arrays[j], N, k);
            if (r) yes++;
            check = (check * 31 + (r ? 1 : 2) + k) % 1000000007;
        }
    }
    printf("250 rounds over 4 arrays of 100000 values: %lld can be divided, checksum %lld\n",
           (long long)yes, (long long)check);
    for (int j = 0; j < ARRAYS; j++) free(arrays[j]);
    return 0;
}
