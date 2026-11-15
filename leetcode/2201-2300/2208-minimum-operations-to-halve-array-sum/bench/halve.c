// benchmark's C mirror of halve.kara (LeetCode #2208, the ★ arm): greedily
// halve the largest number, kept in a hand-written binary max-heap of
// doubles, until the halves taken add up to half the sum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void sift_up(double *h, long i) {
    while (i > 0) {
        long p = (i - 1) / 2;
        if (h[p] >= h[i]) break;
        double t = h[p]; h[p] = h[i]; h[i] = t;
        i = p;
    }
}

static void sift_down(double *h, long n, long i) {
    for (;;) {
        long l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && h[l] > h[m]) m = l;
        if (r < n && h[r] > h[m]) m = r;
        if (m == i) break;
        double t = h[m]; h[m] = h[i]; h[i] = t;
        i = m;
    }
}

static int64_t halve_array(const int64_t *nums, long n) {
    double *h = malloc(sizeof(double) * n);
    long size = 0;
    double total = 0.0;
    for (long i = 0; i < n; i++) {
        total += (double)nums[i];
        h[size] = (double)nums[i];
        sift_up(h, size++);
    }
    double removed = 0.0;
    int64_t ops = 0;
    while (removed < total / 2.0) {
        double top = h[0];        // pop the largest
        h[0] = h[--size];
        sift_down(h, size, 0);
        double half = top / 2.0;
        removed += half;
        h[size] = half;           // and push its half
        sift_up(h, size++);
        ops++;
    }
    free(h);
    return ops;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    int64_t seed = 2208;
    const int64_t tops[3] = {10, 1000, 10000000};
    int64_t *arrays[12];
    for (int a = 0; a < 12; a++) {
        arrays[a] = malloc(sizeof(int64_t) * 100000);
        for (long i = 0; i < 100000; i++) arrays[a][i] = wide_random(&seed) % tops[a % 3] + 1;
    }
    // each array halved once
    int64_t check = 0;
    for (int a = 0; a < 12; a++) check = (check * 31 + halve_array(arrays[a], 100000)) % 1000000007;
    printf("12 arrays of 10^5: checksum %lld\n", (long long)check);
    for (int a = 0; a < 12; a++) free(arrays[a]);
    return 0;
}
