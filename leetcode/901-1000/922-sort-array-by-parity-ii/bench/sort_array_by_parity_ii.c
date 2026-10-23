// LeetCode #922: Sort Array By Parity II -- bench: two pointers, in place.
// Mirrors sort_array_by_parity_ii.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void sort_array_by_parity_ii(int64_t *nums, int64_t n) {
    int64_t j = 1;
    for (int64_t i = 0; i < n; i += 2) {
        if (nums[i] % 2 == 1) {
            while (nums[j] % 2 == 1) j += 2;
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
    }
}

static int64_t seed = 922;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 3000, n = 20000;
    // n / 2 even and n / 2 odd values up to 1000, shuffled, built once
    int64_t *original = malloc(n * sizeof(int64_t));
    for (int64_t k = 0; k < n; k++) {
        int64_t v = 2 * (next_random() % 500);
        original[k] = k % 2 == 0 ? v : v + 1;
    }
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = next_random() % (i + 1);
        int64_t t = original[i];
        original[i] = original[j];
        original[j] = t;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // a fresh copy each round, rearranged, and one value read back
        int64_t *nums = malloc(n * sizeof(int64_t));
        memcpy(nums, original, n * sizeof(int64_t));
        sort_array_by_parity_ii(nums, n);
        check = (check * 1000003 + nums[(r * 7919) % n]) % 1000000007;
        free(nums);
    }
    printf("%lld rounds over %lld values: checksum %lld\n", (long long)rounds, (long long)n, (long long)check);
    free(original);
    return 0;
}
