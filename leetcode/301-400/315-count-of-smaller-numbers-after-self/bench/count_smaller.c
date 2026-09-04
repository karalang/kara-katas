// Benchmark lane for LeetCode 315 — C mirror of bench/count_smaller.kara.
// Generate N values once, then PASSES Fenwick-tree passes (sort+dedup for the
// ranks, then per element a binary search, a prefix query and a point update,
// right to left), each after swapping two elements chosen from the checksum.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 200000
#define PASSES 24
#define MASK 1073741823LL

static long long lcg(long long s) { return (s * 1103515245LL + 12345LL) & 0x7fffffffLL; }

static int cmp_ll(const void* a, const void* b) {
    long long x = *(const long long*)a, y = *(const long long*)b;
    return (x > y) - (x < y);
}

static long long lower_bound(const long long* s, long long len, long long x) {
    long long lo = 0, hi = len;
    while (lo < hi) { long long mid = (lo + hi) / 2; if (s[mid] < x) lo = mid + 1; else hi = mid; }
    return lo;
}

static void count_smaller(const long long* nums, long long n, long long* counts) {
    long long* distinct = malloc(n * sizeof(long long));
    memcpy(distinct, nums, n * sizeof(long long));
    qsort(distinct, n, sizeof(long long), cmp_ll);
    long long m = 0;
    for (long long i = 0; i < n; i++) if (i == 0 || distinct[i] != distinct[i - 1]) distinct[m++] = distinct[i];
    long long* tree = calloc(m + 1, sizeof(long long));
    for (long long i = n - 1; i >= 0; i--) {
        long long r = lower_bound(distinct, m, nums[i]);
        long long total = 0;
        for (long long x = r; x > 0; x -= x & -x) total += tree[x];
        counts[i] = total;
        for (long long x = r + 1; x <= m; x += x & -x) tree[x] += 1;
    }
    free(tree);
    free(distinct);
}

int main(void) {
    long long seed = 315;
    long long* nums = malloc(N * sizeof(long long));
    for (long long i = 0; i < N; i++) { seed = lcg(seed); nums[i] = seed % 200001 - 100000; }
    long long checksum = 0;
    for (int pass = 0; pass < PASSES; pass++) {
        long long i = checksum % N;
        long long j = (checksum * 7 + 13) % N;
        long long t = nums[i]; nums[i] = nums[j]; nums[j] = t;
        long long* counts = malloc(N * sizeof(long long));
        count_smaller(nums, N, counts);
        long long total = 0;
        for (long long k = 0; k < N; k++) total += counts[k];
        free(counts);
        checksum = (checksum * 31 + total) & MASK;
        t = nums[i]; nums[i] = nums[j]; nums[j] = t;
    }
    printf("checksum %lld\n", checksum);
    free(nums);
    return 0;
}
