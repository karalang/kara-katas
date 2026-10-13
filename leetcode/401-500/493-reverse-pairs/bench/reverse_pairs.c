// Benchmark for #493: C mirror of the ★ arm (merge sort); see
// reverse_pairs.kara. Each merge builds its run in a fresh buffer and
// copies it back, as the ★ arm does with a fresh `Vec`.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ARRAYS 60
#define N 50000

static long long sort_count(long long *nums, long long low, long long high) {
    if (high - low <= 1) {
        return 0;
    }
    long long mid = (low + high) / 2;
    long long count = sort_count(nums, low, mid) + sort_count(nums, mid, high);
    long long j = mid;
    for (long long i = low; i < mid; i++) {
        while (j < high && nums[i] > 2 * nums[j]) {
            j++;
        }
        count += j - mid;
    }
    long long *merged = malloc(sizeof(long long) * (high - low));
    long long len = 0, a = low, b = mid;
    while (a < mid || b < high) {
        if (b == high || (a < mid && nums[a] <= nums[b])) {
            merged[len++] = nums[a++];
        } else {
            merged[len++] = nums[b++];
        }
    }
    memcpy(nums + low, merged, sizeof(long long) * len);
    free(merged);
    return count;
}

static long long reverse_pairs(const long long *nums, long long n) {
    long long *work = malloc(sizeof(long long) * n);
    memcpy(work, nums, sizeof(long long) * n);
    long long count = sort_count(work, 0, n);
    free(work);
    return count;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 60 arrays of 50,000 numbers across the whole 32-bit range, built
    // once, then each counted once.
    static long long arrays[ARRAYS][N];
    long long seed = 493;
    for (int k = 0; k < ARRAYS; k++) {
        for (int i = 0; i < N; i++) {
            long long high = next_random(&seed);
            arrays[k][i] = high * 131072 + next_random(&seed) * 4 - 2147483648LL;
        }
    }
    long long total = 0, checksum = 0;
    for (int k = 0; k < ARRAYS; k++) {
        long long pairs = reverse_pairs(arrays[k], N);
        total += pairs;
        checksum = (checksum * 31 + pairs) % 1000000007;
    }
    printf("60 arrays of 50000: %lld reverse pairs, checksum %lld\n", total, checksum);
    return 0;
}
