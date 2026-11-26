// LeetCode #1760: Minimum Limit of Balls in a Bag -- the bench in C,
// mirroring minimum_size.kara: a binary search on the penalty.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t operations(const int *nums, int n, int64_t penalty) {
    int64_t total = 0;
    for (int i = 0; i < n; i++) total += (int64_t)(nums[i] - 1) / penalty;
    return total;
}

static int minimum_size(const int *nums, int n, int max_operations) {
    int lo = 1, hi = nums[0];
    for (int i = 1; i < n; i++) if (nums[i] > hi) hi = nums[i];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (operations(nums, n, mid) <= max_operations) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

int main(void) {
    int64_t seed = 1760;
    int *bags = malloc(sizeof(int) * N);
    for (int i = 0; i < N; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        bags[i] = (int)(1 + (high * 32768 + seed / 65536) % 1000000000);
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 100; call++) {
        int64_t at = (check + call * 7919) % N;
        bags[at] = (int)(1 + (check * 13 + call) % 1000000000);
        int64_t ops = 1 + (check + call * 104729) % 1000000000;
        check = (check * 31 + minimum_size(bags, N, (int)ops)) % 1000000007;
    }
    printf("100 calls over 100000 bags: checksum %lld\n", (long long)check);
    free(bags);
    return 0;
}
