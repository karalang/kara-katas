// LeetCode #2334: Subarray With Elements Greater Than Varying Threshold --
// the bench, the ★ arm in C: the nearest smaller element on either side
// from a monotonic stack, and the widest run whose least element times
// its width exceeds the threshold.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t valid_subarray_size(const int64_t *nums, int64_t n, int64_t threshold) {
    int64_t *left = malloc(n * sizeof(int64_t));
    int64_t *right = malloc(n * sizeof(int64_t));
    int64_t *stack = malloc(n * sizeof(int64_t));
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        left[i] = -1;
        right[i] = n;
    }
    for (int64_t i = 0; i < n; i++) {
        while (top > 0 && nums[stack[top - 1]] >= nums[i]) right[stack[--top]] = i;
        if (top > 0) left[i] = stack[top - 1];
        stack[top++] = i;
    }
    int64_t best = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t width = right[i] - left[i] - 1;
        if (nums[i] * width > threshold && width > best) best = width;
    }
    free(left);
    free(right);
    free(stack);
    return best;
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    static int64_t arrays[10][N];
    for (int64_t a = 0; a < 10; a++)
        for (int64_t i = 0; i < N; i++) arrays[a][i] = scrambled(a * 100000 + i) % 1000000000 + 1;
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++) {
        for (int64_t a = 0; a < 10; a++) {
            int64_t threshold = ((10 * a + p) * 7919 % 1000 + 1) * 1000000;
            check = (check * 31 + valid_subarray_size(arrays[a], N, threshold) + 1) % 1000000007;
        }
    }
    printf("5 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
