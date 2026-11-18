// LeetCode #2321: Maximum Score Of Spliced Array -- the bench, the ★ arm
// in C. Each array's sum plus the largest subarray sum of the
// differences the other array would bring, by Kadane's walk, both ways
// round. O(n).

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t best_gain(const int64_t *into, const int64_t *from, int64_t n) {
    int64_t best = 0, here = 0;
    for (int64_t i = 0; i < n; i++) {
        here = here + from[i] - into[i];
        if (here < 0)
            here = 0;
        if (here > best)
            best = here;
    }
    return best;
}

static int64_t maximums_spliced_array(const int64_t *nums1, const int64_t *nums2, int64_t n) {
    int64_t sum1 = 0, sum2 = 0;
    for (int64_t i = 0; i < n; i++)
        sum1 += nums1[i];
    for (int64_t i = 0; i < n; i++)
        sum2 += nums2[i];
    int64_t one = sum1 + best_gain(nums1, nums2, n);
    int64_t two = sum2 + best_gain(nums2, nums1, n);
    return one > two ? one : two;
}

static int64_t seed = 2321;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *firsts[10], *seconds[10];
    for (int k = 0; k < 10; k++) {
        firsts[k] = malloc(n * sizeof(int64_t));
        seconds[k] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++)
            firsts[k][i] = next_random() % 10000 + 1;
        for (int64_t i = 0; i < n; i++)
            seconds[k][i] = next_random() % 10000 + 1;
    }
    int64_t check = 0;
    for (int p = 0; p < 200; p++)
        for (int k = 0; k < 10; k++) {
            int64_t i = next_random() % n;
            firsts[k][i] = next_random() % 10000 + 1;
            check = (check * 31 + maximums_spliced_array(firsts[k], seconds[k], n)) % 1000000007;
        }
    printf("200 passes over 10 pairs of 10^5 numbers: checksum %lld\n", (long long)check);
    for (int k = 0; k < 10; k++) {
        free(firsts[k]);
        free(seconds[k]);
    }
    return 0;
}
