// LeetCode #2763: Sum of Imbalance Numbers of All Subarrays -- the bench
// (imbalance.kara in C): each index counted for the subarrays in which it
// is the leftmost occurrence of a run's top value, from the last x or
// x + 1 before it and the first x + 1 after it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2763;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t sum_imbalance_numbers(const int64_t *nums, int64_t n, int64_t *left, int64_t *last, int64_t *first) {
    for (int64_t v = 0; v < n + 2; v++) last[v] = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        left[i] = last[x] > last[x + 1] ? last[x] : last[x + 1];
        last[x] = i;
    }
    for (int64_t v = 0; v < n + 2; v++) first[v] = n;
    int64_t total = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t x = nums[i];
        total += (i - left[i]) * (first[x + 1] - i);
        first[x] = i;
    }
    return total - n * (n + 1) / 2;
}

int main(void) {
    const int count = 20000, rounds = 5, n = 1000;
    int64_t *nums = malloc(sizeof(int64_t) * count * n);
    int64_t *left = malloc(sizeof(int64_t) * n);
    int64_t *last = malloc(sizeof(int64_t) * (n + 2));
    int64_t *first = malloc(sizeof(int64_t) * (n + 2));
    for (int64_t k = 0; k < (int64_t)count * n; k++) nums[k] = next_random() % 1000 + 1;
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t found = sum_imbalance_numbers(nums + (int64_t)k * n, n, left, last, first);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    printf("%d arrays of %d, %d rounds: imbalances sum to %lld, checksum %lld\n", count, n, rounds, (long long)sum, (long long)check);
    free(nums); free(left); free(last); free(first);
    return 0;
}
