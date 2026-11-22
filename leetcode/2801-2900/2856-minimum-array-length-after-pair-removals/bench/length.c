// LeetCode #2856: Minimum Array Length After Pair Removals -- the bench:
// the ★ arm over 5000 sorted arrays of 1000 values, each from 1 to k for
// k up to 1000, one time in four with a run of one value making up to
// three quarters, all drawn first, then each answered 50 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_length_after_removals(const int64_t *nums, int64_t n) {
    int64_t most = 0, run = 0;
    for (int64_t i = 0; i < n; i++) {
        run = (i > 0 && nums[i] == nums[i - 1]) ? run + 1 : 1;
        if (run > most) most = run;
    }
    return 2 * most > n ? 2 * most - n : n % 2;
}

static int64_t seed = 2856;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    const int64_t count = 5000, rounds = 50, n = 1000;
    int64_t *arrays = malloc(sizeof(int64_t) * count * n);
    for (int64_t a = 0; a < count; a++) {
        int64_t *nums = arrays + a * n;
        int64_t k = next_random() % 1000 + 1;
        for (int64_t i = 0; i < n; i++) nums[i] = next_random() % k + 1;
        if (next_random() % 4 == 0) {
            int64_t run = next_random() % (3 * n / 4 + 1);
            int64_t v = next_random() % 1000 + 1;
            for (int64_t i = 0; i < run; i++) nums[i] = v;
        }
        qsort(nums, n, sizeof(int64_t), cmp);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t a = 0; a < count; a++) {
            int64_t left = min_length_after_removals(arrays + a * n, n);
            total += left;
            check = (check * 31 + left + r) % 1000000007;
        }
    }
    printf("%lld arrays, %lld rounds: %lld left, checksum %lld\n", (long long)count, (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
