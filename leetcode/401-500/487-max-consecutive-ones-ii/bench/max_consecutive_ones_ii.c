// Benchmark for #487: C mirror of the ★ arm (the run before the
// last 0); see max_consecutive_ones_ii.kara.
#include <stdio.h>
#include <stdlib.h>

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static long long find_max_consecutive_ones(const long long *nums, long long n) {
    long long best = 0, before = 0, run = 0;
    for (long long i = 0; i < n; i++) {
        if (nums[i] == 1) {
            run++;
        } else {
            before = run + 1;
            run = 0;
        }
        if (before + run > best) {
            best = before + run;
        }
    }
    return best;
}

int main(void) {
    long long *arrays[20];
    long long seed = 487, n = 100000;
    for (int a = 0; a < 20; a++) {
        arrays[a] = malloc(sizeof(long long) * n);
        for (long long i = 0; i < n; i++) {
            arrays[a][i] = next_random(&seed) % 100 < 80 + a ? 1 : 0;
        }
    }
    long long total = 0, checksum = 0;
    for (int r = 0; r < 50; r++) {
        for (int a = 0; a < 20; a++) {
            long long best = find_max_consecutive_ones(arrays[a], n);
            total += best;
            checksum = (checksum * 31 + best) % 1000000007;
        }
    }
    printf("1000 scans of 100000 numbers: runs add up to %lld, checksum %lld\n", total, checksum);
    return 0;
}
