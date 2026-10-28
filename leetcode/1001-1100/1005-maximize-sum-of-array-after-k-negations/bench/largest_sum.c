// Benchmark: LeetCode #1005 Maximize Sum Of Array After K Negations -- the
// ★ arm, counting, on arrays of 10000 numbers, LeetCode's longest.
// Mirrors largest_sum.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t largest_sum_after_k_negations(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *count = calloc(201, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[nums[i] + 100]++;
    int64_t left = k;
    int64_t v = -100;
    while (v < 0 && left > 0) {
        int64_t flip = count[v + 100] < left ? count[v + 100] : left;
        count[v + 100] -= flip;
        count[100 - v] += flip;
        left -= flip;
        v++;
    }
    int64_t sum = 0;
    for (v = -100; v < 101; v++) sum += v * count[v + 100];
    if (left % 2 == 1) {
        int64_t smallest = 0;
        while (count[smallest + 100] == 0) smallest++;
        sum -= 2 * smallest;
    }
    free(count);
    return sum;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t rounds = 2500;
    int64_t n = 10000;
    int64_t seed = 1005;
    int64_t *arrays[20];
    for (int64_t t = 0; t < 20; t++) {
        arrays[t] = malloc(n * sizeof(int64_t));
        for (int64_t j = 0; j < n; j++) {
            int64_t size = next_random(&seed) % 101;
            arrays[t][j] = next_random(&seed) % 8 < t % 7 + 1 ? -size : size;
        }
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 20; i++) {
            int64_t t = (r + i) % 20;
            int64_t k = 1 + (r * 37 + t * 101) % 10000;
            int64_t got = largest_sum_after_k_negations(arrays[t], n, k);
            total += got;
            check = (check * 31 + got % 1000000007 + 1000000007) % 1000000007;
        }
    }
    printf("%lld rounds over 20 arrays of %lld numbers: answers sum to %lld, checksum %lld\n",
           (long long)rounds, (long long)n, (long long)total, (long long)check);
    for (int64_t t = 0; t < 20; t++) free(arrays[t]);
    return 0;
}
