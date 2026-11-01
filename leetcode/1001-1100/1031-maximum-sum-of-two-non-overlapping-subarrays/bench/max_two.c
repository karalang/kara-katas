// LeetCode #1031: Maximum Sum of Two Non-Overlapping Subarrays -- bench
// Mirrors ./max_two.kara; see ../README.md § Benchmarks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t max_sum_two_no_overlap(const int64_t *nums, int n, int first_len, int second_len) {
    int64_t *prefix = calloc(n + 1, sizeof(int64_t));
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    int64_t best = 0, best_first = 0, best_second = 0;
    for (int i = first_len + second_len; i <= n; i++) {
        best_first = max64(best_first, prefix[i - second_len] - prefix[i - second_len - first_len]);
        best_second = max64(best_second, prefix[i - first_len] - prefix[i - first_len - second_len]);
        best = max64(best, best_first + prefix[i] - prefix[i - second_len]);
        best = max64(best, best_second + prefix[i] - prefix[i - first_len]);
    }
    free(prefix);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 1000, rounds = 200;
    int64_t seed = 1031;
    static int64_t nums[1000][1000];
    static int first_lens[1000], second_lens[1000];
    for (int k = 0; k < count; k++) {
        for (int i = 0; i < 1000; i++) nums[k][i] = next_random(&seed) % 1001;
        first_lens[k] = (int)(next_random(&seed) % 999 + 1);
        second_lens[k] = (int)(next_random(&seed) % (1000 - first_lens[k]) + 1);
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t answer = max_sum_two_no_overlap(nums[k], 1000, first_lens[k], second_lens[k]);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    printf("%d arrays of 1000 values, %d rounds: sum %lld, checksum %lld\n", count, rounds,
           (long long)total, (long long)check);
    return 0;
}
