// LeetCode #1658: Minimum Operations to Reduce X to Zero -- the bench's C
// mirror: the ★ arm on 1000 random arrays of 100000 numbers from 1 to
// 10000, each x a random prefix plus a random suffix of its array, all
// drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PROBLEMS 1000
#define N 100000

static int32_t min_operations(const int32_t *nums, int64_t n, int32_t x) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int64_t target = total - x;
    if (target < 0) return -1;
    int64_t longest = -1, sum = 0, left = 0;
    for (int64_t right = 0; right < n; right++) {
        sum += nums[right];
        while (sum > target) {
            sum -= nums[left];
            left += 1;
        }
        if (sum == target && right - left + 1 > longest) longest = right - left + 1;
    }
    return longest < 0 ? -1 : (int32_t)(n - longest);
}

static int64_t seed = 1658;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *nums = malloc(sizeof(int32_t) * PROBLEMS * N);
    int32_t xs[PROBLEMS];
    for (int p = 0; p < PROBLEMS; p++) {
        int32_t *a = nums + (int64_t)p * N;
        for (int i = 0; i < N; i++) a[i] = (int32_t)(next_random() % 10000 + 1);
        int64_t left = next_random() % 1000, right = next_random() % 1000;
        int64_t x = 0;
        for (int64_t i = 0; i < left; i++) x += a[i];
        for (int64_t i = N - right; i < N; i++) x += a[i];
        xs[p] = (int32_t)(x > 1 ? x : 1);
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < PROBLEMS; p++) {
        int64_t answer = min_operations(nums + (int64_t)p * N, N, xs[p]);
        total += answer;
        check = (check * 31 + answer + 2) % 1000000007;
    }
    free(nums);
    printf("1000 arrays of 100000 numbers: operations sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
