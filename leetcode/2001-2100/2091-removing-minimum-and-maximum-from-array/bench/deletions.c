// LeetCode #2091: Removing Minimum and Maximum From Array -- C mirror of
// the ★ arm's benchmark (deletions.kara): the same 20 shuffled arrays, each
// answered 20 times by the same walk over a `malloc`'d array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2091;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t min2(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t minimum_deletions(const int64_t *nums, int64_t n) {
    int64_t lo = 0, hi = 0;
    for (int64_t k = 1; k < n; k++) {
        if (nums[k] < nums[lo]) lo = k;
        if (nums[k] > nums[hi]) hi = k;
    }
    int64_t i = min2(lo, hi), j = lo > hi ? lo : hi;
    return min2(min2(j + 1, n - i), i + 1 + n - j);
}

int main(void) {
    int64_t *arrays = malloc((size_t)20 * N * sizeof(int64_t));
    for (int t = 0; t < 20; t++) {
        int64_t *v = arrays + (size_t)t * N;
        for (int64_t i = 0; i < N; i++) v[i] = 2 * i - 100000;
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t x = v[i];
            v[i] = v[j];
            v[j] = x;
        }
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 20; round++) {
        for (int t = 0; t < 20; t++) {
            int64_t d = minimum_deletions(arrays + (size_t)((t + round) % 20) * N, N);
            total += d;
            check = (check * 31 + d) % 1000000007;
        }
    }
    printf("400 answers: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(arrays);
    return 0;
}
