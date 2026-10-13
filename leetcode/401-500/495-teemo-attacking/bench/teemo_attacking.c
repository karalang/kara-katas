// Benchmark for #495: C mirror of the ★ arm (each gap, capped); see
// teemo_attacking.kara.
#include <stdio.h>

#define SERIES 200
#define N 10000

static long long find_poisoned_duration(const long long *series, long long n, long long duration) {
    long long total = 0;
    for (long long i = 0; i < n; i++) {
        if (i + 1 < n) {
            long long gap = series[i + 1] - series[i];
            total += gap < duration ? gap : duration;
        } else {
            total += duration;
        }
    }
    return total;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 200 series of 10,000 attacks (the problem's most) with gaps of 0
    // to 99, built once, then each solved for every duration from 0 to
    // 49.
    static long long all[SERIES][N];
    long long seed = 495;
    for (int k = 0; k < SERIES; k++) {
        long long t = 0;
        for (int i = 0; i < N; i++) {
            all[k][i] = t;
            t += next_random(&seed) % 100;
        }
    }
    long long total = 0, checksum = 0;
    for (int k = 0; k < SERIES; k++) {
        for (long long duration = 0; duration < 50; duration++) {
            long long poisoned = find_poisoned_duration(all[k], N, duration);
            total += poisoned;
            checksum = (checksum * 31 + poisoned) % 1000000007;
        }
    }
    printf("200 series of 10000, 50 durations each: %lld poisoned in all, checksum %lld\n", total, checksum);
    return 0;
}
