// Benchmark: LeetCode #1004 Max Consecutive Ones III -- the ★ arm, a
// sliding window, on arrays of 100000 numbers, LeetCode's longest.
// Mirrors longest_ones.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_ones(const int64_t *nums, int64_t n, int64_t k) {
    int64_t left = 0, zeros = 0, best = 0;
    for (int64_t right = 0; right < n; right++) {
        if (nums[right] == 0) zeros++;
        while (zeros > k) {
            if (nums[left] == 0) zeros--;
            left++;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t rounds = 30, n = 100000;
    int64_t seed = 1004;
    int64_t *arrays[20];
    for (int64_t t = 0; t < 20; t++) {
        arrays[t] = malloc(n * sizeof(int64_t));
        for (int64_t j = 0; j < n; j++)
            arrays[t][j] = next_random(&seed) % 8 < t % 7 + 1 ? 1 : 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 20; i++) {
            int64_t t = (r + i) % 20;
            int64_t k = (r * 37 + t * 101) % 3000;
            int64_t got = longest_ones(arrays[t], n, k);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("%lld rounds over 20 arrays of %lld numbers: answers sum to %lld, checksum %lld\n",
           (long long)rounds, (long long)n, (long long)total, (long long)check);
    for (int t = 0; t < 20; t++) free(arrays[t]);
    return 0;
}
