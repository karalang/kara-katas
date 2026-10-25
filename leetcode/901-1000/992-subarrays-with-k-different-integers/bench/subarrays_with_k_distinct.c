// LeetCode #992: Subarrays with K Different Integers -- bench, the ★ arm
// (at most k, less at most k - 1), the same algorithm and workload as
// subarrays_with_k_distinct.kara. Each count array is allocated and
// zeroed per call, as the Kāra arm's `Vec.filled` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t at_most(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *count = calloc(n + 1, sizeof(int64_t));
    int64_t distinct = 0, left = 0, total = 0;
    for (int64_t right = 0; right < n; right++) {
        if (count[nums[right]] == 0) distinct += 1;
        count[nums[right]] += 1;
        while (distinct > k) {
            count[nums[left]] -= 1;
            if (count[nums[left]] == 0) distinct -= 1;
            left += 1;
        }
        total += right - left + 1;
    }
    free(count);
    return total;
}

static int64_t subarrays_with_k_distinct(const int64_t *nums, int64_t n, int64_t k) {
    return at_most(nums, n, k) - at_most(nums, n, k - 1);
}

static int64_t seed = 992;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t arrays[20][20000];

int main(void) {
    int rounds = 100;
    for (int i = 0; i < 20; i++)
        for (int j = 0; j < 20000; j++) arrays[i][j] = 1 + next_random() % 100;
    int64_t found = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t k = 1 + (r * 7 + i) % 60;
            int64_t got = subarrays_with_k_distinct(arrays[(r + i) % 20], 20000, k);
            found += got;
            check = (check * 31 + got + 1) % 1000000007;
        }
    }
    printf("%d rounds over 20 arrays of 20000 numbers: %lld subarrays, checksum %lld\n", rounds,
           (long long)found, (long long)check);
    return 0;
}
