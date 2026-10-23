// LeetCode #907: Sum of Subarray Minimums -- bench program, C.
//
// How far each element reaches, over 1,000,000 numbers from 1 to 30000
// built once. Each round sums the subarray minimums, folds the sum into a
// checksum and changes one number.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t sum_subarray_mins(const int64_t *arr, int64_t n) {
    int64_t *left = calloc(n, sizeof(int64_t));
    int64_t *right = calloc(n, sizeof(int64_t));
    int64_t *stack = malloc(sizeof(int64_t) * n);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        while (top > 0 && arr[stack[top - 1]] >= arr[i]) top -= 1;
        left[i] = top > 0 ? i - stack[top - 1] : i + 1;
        stack[top++] = i;
    }
    top = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t i = n - 1 - k;
        while (top > 0 && arr[stack[top - 1]] > arr[i]) top -= 1;
        right[i] = top > 0 ? stack[top - 1] - i : n - i;
        stack[top++] = i;
    }
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total = (total + arr[i] * left[i] % 1000000007 * right[i]) % 1000000007;
    }
    free(left);
    free(right);
    free(stack);
    return total;
}

static int64_t seed = 907;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 1000000;
    int64_t rounds = 40;
    int64_t *arr = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) arr[i] = 1 + next_random() % 30000;
    int64_t check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t got = sum_subarray_mins(arr, n);
        check = (check * 31 + got) % 1000000007;
        arr[round * 7919 % n] = 1 + next_random() % 30000;
    }
    printf("%lld rounds over %lld numbers: checksum %lld\n", (long long)rounds, (long long)n, (long long)check);
    free(arr);
    return 0;
}
