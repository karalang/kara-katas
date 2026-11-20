// LeetCode #1712: Ways to Split Array Into Three Subarrays -- the C mirror
// of the bench (split.kara): prefix sums, and for each end of the left
// part two binary searches, on 20 random arrays of 100000 values, each
// answered 10 times.
#include <stdio.h>
#include <stdlib.h>

// the first index whose prefix is at least `bound`, as partition_point
// with `p < bound`
static long first_at_least(const long long *prefix, long len, long long bound) {
    long lo = 0;
    long hi = len;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        if (prefix[mid] < bound) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

// the first index whose doubled prefix passes `bound`, as partition_point
// with `2 * p <= bound`
static long first_twice_above(const long long *prefix, long len, long long bound) {
    long lo = 0;
    long hi = len;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        if (2 * prefix[mid] <= bound) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

static int ways_to_split(const int *nums, long n) {
    long long *prefix = malloc(sizeof(long long) * (n + 1));
    prefix[0] = 0;
    for (long i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    long long total = prefix[n];
    long long ways = 0;
    for (long i = 1; i < n - 1; i++) {
        long long left = prefix[i];
        long lo = first_at_least(prefix, n + 1, 2 * left);
        if (lo < i + 1) {
            lo = i + 1;
        }
        long hi = first_twice_above(prefix, n + 1, total + left);
        if (hi > n) {
            hi = n;
        }
        if (hi > lo) {
            ways += hi - lo;
        }
    }
    free(prefix);
    return (int)(ways % 1000000007);
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 20;
    const long long rounds = 10;
    const long n = 100000;
    long long seed = 1712;
    int *arrays = malloc(sizeof(int) * count * n);
    for (long i = 0; i < count * n; i++) {
        arrays[i] = (int)(next_random(&seed) % 10001);
    }
    long long sum = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long long answer = ways_to_split(arrays + p * n, n);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d arrays of %ld values, %lld rounds: answers sum to %lld, checksum %lld\n", count, n, rounds, sum, check);
    free(arrays);
    return 0;
}
