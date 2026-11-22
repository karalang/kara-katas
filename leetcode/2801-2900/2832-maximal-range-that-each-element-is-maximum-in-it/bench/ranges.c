// LeetCode #2832: Maximal Range That Each Element Is Maximum in It --
// the bench, mirrored from ranges.kara: two passes of a falling stack.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t *maximum_length_of_ranges(const int64_t *nums, int64_t n) {
    int64_t *left = malloc(sizeof(int64_t) * n);
    int64_t *right = malloc(sizeof(int64_t) * n);
    int64_t *stack = malloc(sizeof(int64_t) * n);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        while (top > 0 && nums[stack[top - 1]] <= nums[i]) top--;
        left[i] = top > 0 ? stack[top - 1] : -1;
        stack[top++] = i;
    }
    top = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        while (top > 0 && nums[stack[top - 1]] <= nums[i]) top--;
        right[i] = top > 0 ? stack[top - 1] : n;
        stack[top++] = i;
    }
    int64_t *ans = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) ans[i] = right[i] - left[i] - 1;
    free(left); free(right); free(stack);
    return ans;
}

int main(void) {
    const int64_t count = 20, rounds = 20, n = 100000;
    int64_t seed = 2832;
    int64_t *arrays = malloc(sizeof(int64_t) * count * n);
    for (int64_t c = 0; c < count; c++) {
        int64_t *nums = arrays + c * n;
        for (int64_t i = 0; i < n; i++) nums[i] = i + 1;
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t hi = next_random(&seed);
            int64_t j = (hi * 32768 + next_random(&seed)) % (i + 1);
            int64_t t = nums[i]; nums[i] = nums[j]; nums[j] = t;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t *ans = maximum_length_of_ranges(arrays + c * n, n);
            for (int64_t i = 0; i < n; i++) {
                total += ans[i];
                check = (check * 31 + ans[i] + r) % 1000000007;
            }
            free(ans);
        }
    }
    printf("%lld arrays of %lld, %lld rounds: ranges total %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
