// LeetCode #2302: Count Subarrays With Score Less Than K -- the bench,
// the ★ arm in C. A sliding window, narrowed at the left while its score
// is k or more, counting every subarray ending at its right end.
#include <stdint.h>
#include <stdio.h>

enum { ARRAYS = 20, N = 100000 };

static int64_t count_subarrays(const int64_t *nums, int64_t n, int64_t k) {
    int64_t count = 0, sum = 0, left = 0;
    for (int64_t right = 0; right < n; right++) {
        sum += nums[right];
        while (sum * (right - left + 1) >= k) {
            sum -= nums[left];
            left++;
        }
        count += right - left + 1;
    }
    return count;
}

static int64_t seed = 2302;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[ARRAYS][N];
    for (int a = 0; a < ARRAYS; a++)
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            arrays[a][i] = (hi * 32768 + next_random()) % 100000 + 1;
        }
    int64_t check = 0;
    for (int64_t p = 0; p < 30; p++)
        for (int64_t a = 0; a < ARRAYS; a++)
            check = (check * 31 + count_subarrays(arrays[a], N, 1000000000LL * (a + 1) + p)) % 1000000007;
    printf("30 passes over 20 arrays of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
