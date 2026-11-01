// LeetCode #1035: Uncrossed Lines -- bench
// Mirrors ./uncrossed_lines.kara; see ../README.md § Benchmarks. The
// table is one calloc'd block per call, where the Kāra and Rust versions
// allocate a row at a time.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_uncrossed_lines(const int64_t *nums1, int64_t m, const int64_t *nums2, int64_t n) {
    int64_t w = n + 1;
    int64_t *best = calloc((size_t)((m + 1) * w), sizeof(int64_t));
    for (int64_t i = 1; i <= m; i++) {
        for (int64_t j = 1; j <= n; j++) {
            if (nums1[i - 1] == nums2[j - 1]) {
                best[i * w + j] = best[(i - 1) * w + j - 1] + 1;
            } else {
                int64_t up = best[(i - 1) * w + j], left = best[i * w + j - 1];
                best[i * w + j] = up > left ? up : left;
            }
        }
    }
    int64_t answer = best[m * w + n];
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 40, rounds = 20;
    int64_t seed = 1035;
    static int64_t nums1[40][500], nums2[40][500];
    for (int p = 0; p < count; p++) {
        for (int i = 0; i < 500; i++) nums1[p][i] = next_random(&seed) % 10 + 1;
        for (int i = 0; i < 500; i++) nums2[p][i] = next_random(&seed) % 10 + 1;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            int64_t lines = max_uncrossed_lines(nums1[p], 500, nums2[p], 500);
            total += lines;
            check = (check * 131 + lines) % 1000000007;
        }
    }
    printf("%d pairs of 500 values, %d rounds: sum %lld, checksum %lld\n", count, rounds, (long long)total, (long long)check);
    return 0;
}
