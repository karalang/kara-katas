// LeetCode #1150: Check If a Number Is Majority Element in a Sorted Array
// -- the C mirror of the ★ arm: the run's start by a binary search for the
// first value not below the target, then the value n / 2 places on.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int is_majority_element(const int64_t *nums, int64_t n, int64_t target) {
    int64_t low = 0, high = n;
    while (low < high) {
        int64_t mid = low + (high - low) / 2;
        if (nums[mid] < target) low = mid + 1;
        else high = mid;
    }
    return low + n / 2 < n && nums[low + n / 2] == target;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t big(int64_t *seed) {
    int64_t a = next_random(seed);
    return (a * 32768 + next_random(seed)) % 1000000000 + 1;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static void list(int64_t *seed, int64_t *nums) {
    int64_t copies = 450 + next_random(seed) % 101;
    int64_t v = big(seed);
    for (int64_t i = 0; i < copies; i++) nums[i] = v;
    for (int64_t i = copies; i < 1000; i++) nums[i] = big(seed);
    qsort(nums, 1000, sizeof(int64_t), cmp);
}

int main(void) {
    int64_t seed = 1150;
    static int64_t lists[64][1000];
    for (int i = 0; i < 64; i++) list(&seed, lists[i]);
    int64_t yes = 0, check = 0;
    for (int64_t q = 0; q < 10000000; q++) {
        const int64_t *nums = lists[q % 64];
        int64_t kind = next_random(&seed) % 4, target;
        if (kind == 0) target = nums[next_random(&seed) % 1000];
        else if (kind == 1) target = nums[500];
        else if (kind == 2) target = nums[next_random(&seed) % 1000] + 1;
        else target = big(&seed);
        if (is_majority_element(nums, 1000, target)) {
            yes++;
            check = (check * 31 + q) % 1000000007;
        }
    }
    printf("10000000 queries over 64 lists of 1000 values: majority %lld, checksum %lld\n", (long long)yes, (long long)check);
    return 0;
}
