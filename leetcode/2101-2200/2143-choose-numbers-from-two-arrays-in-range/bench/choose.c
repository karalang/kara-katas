// LeetCode #2143: Choose Numbers From Two Arrays in Range -- the
// benchmark, the same algorithm as choose.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100

static int64_t count_subranges(const int64_t *nums1, const int64_t *nums2, int64_t n) {
    const int64_t modulus = 1000000007;
    int64_t low = 0, high = 0;
    for (int64_t i = 0; i < n; i++) {
        low += nums2[i];
        high += nums1[i];
    }
    int64_t width = low + high + 1;
    int64_t *ways = calloc(width, sizeof(int64_t));
    int64_t balanced = 0;
    for (int64_t i = 0; i < n; i++) {
        ways[low] += 1;
        int64_t *next = calloc(width, sizeof(int64_t));
        for (int64_t d = 0; d < width; d++) {
            if (ways[d] > 0) {
                next[d + nums1[i]] = (next[d + nums1[i]] + ways[d]) % modulus;
                next[d - nums2[i]] = (next[d - nums2[i]] + ways[d]) % modulus;
            }
        }
        free(ways);
        ways = next;
        balanced = (balanced + ways[low]) % modulus;
    }
    free(ways);
    return balanced;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2143;
    int64_t firsts[4][N], seconds[4][N];
    for (int p = 0; p < 4; p++) {
        for (int i = 0; i < N; i++) firsts[p][i] = next_random(&seed) % 101;
        for (int i = 0; i < N; i++) seconds[p][i] = next_random(&seed) % 101;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 50; round++) {
        for (int p = 0; p < 4; p++) {
            int64_t at = next_random(&seed) % N;
            firsts[p][at] = next_random(&seed) % 101;
            seconds[p][at] = next_random(&seed) % 101;
            int64_t ways = count_subranges(firsts[p], seconds[p], N);
            total += ways;
            check = (check * 31 + ways + round) % 1000000007;
        }
    }
    printf("200 solves: %lld ranges in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
