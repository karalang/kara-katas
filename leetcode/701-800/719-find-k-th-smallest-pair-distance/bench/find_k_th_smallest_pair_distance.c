// LeetCode #719: Find K-th Smallest Pair Distance -- binary search on
// the distance. Benchmark mirror of the Kara star arm: sort a copy,
// then find the least distance with at least k pairs, counting pairs
// with two pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t smallest_distance_pair(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *sorted = malloc(n * sizeof(int64_t));
    memcpy(sorted, nums, n * sizeof(int64_t));
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t lo = 0, hi = sorted[n - 1] - sorted[0];
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        int64_t count = 0, left = 0;
        for (int64_t right = 0; right < n; right++) {
            while (sorted[right] - sorted[left] > mid) left++;
            count += right - left;
        }
        if (count >= k) hi = mid;
        else lo = mid + 1;
    }
    free(sorted);
    return lo;
}

enum { ARRAYS = 40, N = 5000 };

int main(void) {
    int64_t seed = 719;
    static int64_t arrays[ARRAYS][N];
    for (int a = 0; a < ARRAYS; a++)
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            arrays[a][i] = (hi * 32768 + lo) % 1000001;
        }
    int64_t pairs = (int64_t)N * (N - 1) / 2;
    int64_t sum = 0;
    for (int64_t round = 0; round < 25; round++)
        for (int64_t a = 0; a < ARRAYS; a++) {
            int64_t k = 1 + (round * 7919 + a * 104729) % pairs;
            sum += smallest_distance_pair(arrays[a], N, k);
        }
    printf("25 rounds of 40 arrays of 5000 numbers: sum %lld\n", (long long)sum);
    return 0;
}
