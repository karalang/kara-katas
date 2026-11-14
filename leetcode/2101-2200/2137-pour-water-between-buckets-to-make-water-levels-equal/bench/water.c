// LeetCode #2137: Pour Water Between Buckets to Make Water Levels Equal --
// the benchmark, the same algorithm as water.kara. The pour's product is
// its own statement so that no compiler fuses it with the sum: every
// language here rounds the same steps.
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static double equalize_water(const int64_t *buckets, int64_t n, int64_t loss) {
    double keep = (double)(100 - loss) / 100.0;
    int64_t fullest = buckets[0];
    for (int64_t i = 1; i < n; i++)
        if (buckets[i] > fullest) fullest = buckets[i];
    double low = 0.0, high = (double)fullest;
    for (int k = 0; k < 64; k++) {
        double mid = (low + high) / 2.0;
        double spare = 0.0, need = 0.0;
        for (int64_t i = 0; i < n; i++) {
            double w = (double)buckets[i];
            if (w > mid) {
                double poured = (w - mid) * keep;
                spare += poured;
            } else {
                need += mid - w;
            }
        }
        if (spare >= need) low = mid;
        else high = mid;
    }
    return low;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2137;
    int64_t *lists[10];
    for (int l = 0; l < 10; l++) {
        lists[l] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) lists[l][i] = next_random(&seed) % 100001;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int l = 0; l < 10; l++) {
            int64_t hi = next_random(&seed);
            int64_t at = (hi * 32768 + next_random(&seed)) % N;
            lists[l][at] = next_random(&seed) % 100001;
            int64_t loss = next_random(&seed) % 100;
            double level = equalize_water(lists[l], N, loss);
            int64_t scaled = (int64_t)floor(level * 1048576.0 + 0.5);
            total += scaled;
            check = (check * 31 + scaled + round) % 1000000007;
        }
    }
    printf("100 solves: %lld in all, in steps of 2^-20, checksum %lld\n", (long long)total, (long long)check);
    for (int l = 0; l < 10; l++) free(lists[l]);
    return 0;
}
