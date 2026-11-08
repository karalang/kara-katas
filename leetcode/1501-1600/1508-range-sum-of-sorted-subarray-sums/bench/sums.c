// LeetCode #1508: Range Sum of Sorted Subarray Sums -- the bench: 40 arrays
// of 1000 numbers built once, then 25 ranges of places asked of each, by
// the ★ arm.
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007L

static void at_most(const long *prefix, const long *twice, long n, long bound, long *count, long *total) {
    long c = 0, t = 0, i = 0;
    for (long j = 1; j <= n; j++) {
        while (prefix[j] - prefix[i] > bound) i++;
        c += j - i;
        t += (j - i) * prefix[j] - (twice[j] - twice[i]);
    }
    *count = c;
    *total = t;
}

static long smallest(const long *prefix, const long *twice, long n, long k) {
    if (k == 0) return 0;
    long lo = 1, hi = prefix[n], count, total;
    while (lo < hi) {
        long mid = (lo + hi) / 2;
        at_most(prefix, twice, n, mid, &count, &total);
        if (count >= k) hi = mid;
        else lo = mid + 1;
    }
    at_most(prefix, twice, n, lo, &count, &total);
    return total - (count - k) * lo;
}

static long range_sum(const long *nums, long n, long left, long right) {
    long *prefix = calloc(n + 1, sizeof(long));
    long *twice = calloc(n + 1, sizeof(long));
    for (long i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    for (long i = 0; i < n; i++) twice[i + 1] = twice[i] + prefix[i];
    long r = (smallest(prefix, twice, n, right) - smallest(prefix, twice, n, left - 1)) % MOD;
    free(prefix);
    free(twice);
    return r;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    long seed = 1508;
    static long arrays[40][1000];
    for (int a = 0; a < 40; a++)
        for (int i = 0; i < 1000; i++) arrays[a][i] = next_random(&seed) % 100 + 1;
    long total = 1000 * 1001 / 2, check = 0;
    for (int r = 0; r < 25; r++) {
        for (int k = 0; k < 40; k++) {
            long a = next_random(&seed) % total + 1;
            long b = next_random(&seed) % total + 1;
            long lo = a < b ? a : b, hi = a < b ? b : a;
            check = (check * 31 + range_sum(arrays[k], 1000, lo, hi) + 1) % 1000000007;
        }
    }
    printf("1000 ranges over 40 arrays of 1000 numbers: checksum %ld\n", check);
    return 0;
}
