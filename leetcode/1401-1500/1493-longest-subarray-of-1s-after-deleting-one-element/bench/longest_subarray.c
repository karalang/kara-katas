// LeetCode #1493: Longest Subarray of 1's After Deleting One Element -- the
// bench in C, mirroring longest_subarray.kara: a sliding window holding at
// most one 0.
#include <stdint.h>
#include <stdio.h>

#define N 100000

static int32_t longest_subarray(const int32_t *nums, int64_t n) {
    int64_t best = 0, zeros = 0, left = 0;
    for (int64_t right = 0; right < n; right++) {
        if (nums[right] == 0) zeros++;
        while (zeros > 1) {
            if (nums[left] == 0) zeros--;
            left++;
        }
        if (right - left > best) best = right - left;
    }
    return (int32_t)best;
}

static int32_t nums[N];

int main(void) {
    int64_t seed = 1493;
    for (int64_t i = 0; i < N; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        nums[i] = seed / 65536 % 10 == 0 ? 0 : 1;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 1000; call++) {
        int64_t at = (check + call * 7919) % N;
        nums[at] = 1 - nums[at];
        check = (check * 31 + longest_subarray(nums, N) + 1) % 1000000007;
    }
    printf("1000 calls over 100000 digits: checksum %lld\n", (long long)check);
    return 0;
}
