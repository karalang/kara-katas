// LeetCode #2717: Semi-Ordered Permutation -- the bench (semi.kara in C):
// 1's index plus n's distance from the end, less one when 1 starts right
// of n, each index found by a scan.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t position(const int64_t *nums, int64_t n, int64_t value) {
    for (int64_t i = 0; i < n; i++)
        if (nums[i] == value) return i;
    abort();
}

static int64_t semi_ordered_permutation(const int64_t *nums, int64_t n) {
    int64_t first = position(nums, n, 1);
    int64_t last = position(nums, n, n);
    int64_t swaps = first + (n - 1 - last);
    return first > last ? swaps - 1 : swaps;
}

static int64_t seed = 2717;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 200000, rounds = 20, n = 50;
    int64_t *perms = malloc(sizeof(int64_t) * (size_t)count * n);
    for (int k = 0; k < count; k++) {
        int64_t *nums = perms + (size_t)k * n;
        for (int i = 0; i < n; i++) nums[i] = i + 1;
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t swaps = semi_ordered_permutation(perms + (size_t)k * n, n);
            sum += swaps;
            check = (check * 31 + swaps + r) % 1000000007;
        }
    }
    printf("%d permutations of 50, %d rounds: swaps sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(perms);
    return 0;
}
