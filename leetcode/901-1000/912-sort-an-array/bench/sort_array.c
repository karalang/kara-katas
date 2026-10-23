// LeetCode #912: Sort an Array -- bench program, C.
//
// Heap sort on 500,000 numbers from -5 * 10^4 to 5 * 10^4, built once.
// Each round sorts a copy, folds a sample of the sorted values into a
// checksum and changes one number; 6 rounds.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void sift_down(int64_t *a, int64_t start, int64_t end) {
    int64_t root = start;
    for (;;) {
        int64_t child = 2 * root + 1;
        if (child >= end) return;
        if (child + 1 < end && a[child + 1] > a[child]) child++;
        if (a[root] >= a[child]) return;
        int64_t held = a[root];
        a[root] = a[child];
        a[child] = held;
        root = child;
    }
}

static int64_t *sort_array(const int64_t *nums, int64_t n) {
    int64_t *a = malloc(sizeof(int64_t) * n);
    memcpy(a, nums, sizeof(int64_t) * n);
    for (int64_t parent = n / 2 - 1; parent >= 0; parent--) sift_down(a, parent, n);
    for (int64_t end = n - 1; end > 0; end--) {
        int64_t top = a[0];
        a[0] = a[end];
        a[end] = top;
        sift_down(a, 0, end);
    }
    return a;
}

static int64_t seed = 912;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 500000;
    int64_t rounds = 6;
    int64_t *nums = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) nums[i] = next_random() % 100001 - 50000;
    int64_t check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t *sorted = sort_array(nums, n);
        for (int64_t i = round; i < n; i += 997) check = (check * 31 + sorted[i] + 50000) % 1000000007;
        free(sorted);
        nums[round * 7919 % n] = next_random() % 100001 - 50000;
    }
    printf("%lld rounds over %lld numbers: checksum %lld\n", (long long)rounds, (long long)n, (long long)check);
    free(nums);
    return 0;
}
