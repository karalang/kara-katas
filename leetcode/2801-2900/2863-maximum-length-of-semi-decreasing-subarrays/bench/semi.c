// LeetCode #2863: Maximum Length of Semi-Decreasing Subarrays -- the
// bench: the ★ arm over 100 arrays of 10^5 values, LeetCode's most,
// every other one random over LeetCode's range and the rest rising with
// five values moved, all drawn first, then each answered 10 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_subarray_length(const int64_t *nums, int64_t n, int64_t *starts) {
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++)
        if (top == 0 || nums[i] > nums[starts[top - 1]]) starts[top++] = i;
    int64_t best = 0;
    for (int64_t j = n - 1; j >= 0; j--) {
        while (top > 0) {
            int64_t i = starts[top - 1];
            if (nums[i] <= nums[j]) break;
            if (j - i + 1 > best) best = j - i + 1;
            top--;
        }
    }
    return best;
}

static int64_t seed = 2863;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 100, rounds = 10, n = 100000;
    int64_t *arrays = malloc(sizeof(int64_t) * count * n), *starts = malloc(sizeof(int64_t) * n);
    for (int64_t c = 0; c < count; c++) {
        int64_t *nums = arrays + c * n;
        for (int64_t i = 0; i < n; i++) nums[i] = c % 2 == 0 ? wide() % 2000000001 - 1000000000 : 20000 * i - 1000000000;
        if (c % 2 == 1) {
            for (int k = 0; k < 5; k++) {
                int64_t i = wide() % n;
                nums[i] = wide() % 2000000001 - 1000000000;
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t longest = max_subarray_length(arrays + c * n, n, starts);
            total += longest;
            check = (check * 31 + longest + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: lengths total %lld, checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    free(starts);
    return 0;
}
