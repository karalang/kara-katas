// LeetCode #2104: Sum of Subarray Ranges -- bench, C mirror of
// ranges.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t sub_array_ranges(const int64_t *nums, int64_t n, int64_t *stack) {
    int64_t sum = 0, top_n = 0;
    for (int64_t i = 0; i <= n; i++) {
        while (top_n > 0 && (i == n || nums[stack[top_n - 1]] < nums[i])) {
            int64_t top = stack[--top_n];
            int64_t left = top_n > 0 ? stack[top_n - 1] : -1;
            sum += nums[top] * (top - left) * (i - top);
        }
        stack[top_n++] = i;
    }
    top_n = 0;
    for (int64_t i = 0; i <= n; i++) {
        while (top_n > 0 && (i == n || nums[stack[top_n - 1]] > nums[i])) {
            int64_t top = stack[--top_n];
            int64_t left = top_n > 0 ? stack[top_n - 1] : -1;
            sum -= nums[top] * (top - left) * (i - top);
        }
        stack[top_n++] = i;
    }
    return sum;
}

static int64_t seed = 2104;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

int main(void) {
    int64_t *arrays = malloc(sizeof(int64_t) * 1000 * 1000);
    int64_t stack[1001];
    for (int a = 0; a < 1000; a++)
        for (int k = 0; k < 1000; k++)
            arrays[a * 1000 + k] = wide_random() % 2000000001 - 1000000000;
    int64_t total = 0, check = 0;
    for (int p = 0; p < 10; p++)
        for (int a = 0; a < 1000; a++) {
            int64_t got = sub_array_ranges(arrays + a * 1000, 1000, stack) % 1000000007;
            total = (total + got) % 1000000007;
            check = (check * 31 + got) % 1000000007;
        }
    printf("10000 arrays: total %lld, checksum %lld\n", (long long)total, (long long)check);
    free(arrays);
    return 0;
}
