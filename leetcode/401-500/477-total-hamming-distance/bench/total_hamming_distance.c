// Benchmark for #477: C mirror of the ★ arm (one bit at a time); see
// total_hamming_distance.kara.
#include <stdio.h>

static long long total_hamming_distance(const long long *nums, int n) {
    long long total = 0;
    for (int bit = 0; bit < 30; bit++) {
        long long ones = 0;
        for (int i = 0; i < n; i++) {
            ones += (nums[i] >> bit) & 1;
        }
        total += ones * (n - ones);
    }
    return total;
}

static long long seed = 477;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long nums[10000];

int main(void) {
    int n = 10000;
    int rounds = 5000;
    for (int i = 0; i < n; i++) {
        long long a = next_random();
        long long b = next_random();
        nums[i] = (a * 32768 + b) % 1000000001;
    }
    long long total = 0, checksum = 0;
    for (int r = 0; r < rounds; r++) {
        long long a = next_random();
        long long b = next_random();
        nums[r % n] = (a * 32768 + b) % 1000000001;
        long long got = total_hamming_distance(nums, n);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%d rounds on %d numbers: distances add up to %lld, checksum %lld\n", rounds, n, total, checksum);
    return 0;
}
