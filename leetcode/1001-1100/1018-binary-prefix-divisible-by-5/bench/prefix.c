// LeetCode #1018: Binary Prefix Divisible By 5 -- bench
// Mirrors prefix.kara; see ../README.md § Benchmarks.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// answers for nums[0..len), in a fresh array the caller frees
static bool *prefixes_div_by5(const int64_t *nums, int64_t len) {
    bool *answer = malloc((size_t)len * sizeof(bool));
    int64_t r = 0;
    for (int64_t i = 0; i < len; i++) {
        r = (r * 2 + nums[i]) % 5;
        answer[i] = r == 0;
    }
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t len = 2000000;
    int64_t rounds = 50;
    int64_t seed = 1018;
    int64_t *nums = malloc((size_t)len * sizeof(int64_t));
    for (int64_t i = 0; i < len; i++) {
        nums[i] = next_random(&seed) % 2;
    }
    int64_t trues = 0;
    int64_t sum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t at = round * 39989 % len;
        nums[at] = 1 - nums[at];
        bool *answer = prefixes_div_by5(nums, len);
        for (int64_t i = 0; i < len; i++) {
            if (answer[i]) {
                trues++;
                sum = (sum + i) % 1000000007;
            }
        }
        free(answer);
    }
    printf("%lld rounds over %lld bits: %lld true, index sum %lld\n", (long long)rounds,
           (long long)len, (long long)trues, (long long)sum);
    free(nums);
    return 0;
}
