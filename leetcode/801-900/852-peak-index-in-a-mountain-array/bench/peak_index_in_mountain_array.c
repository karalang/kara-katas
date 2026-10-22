// Benchmark for #852: Peak Index in a Mountain Array -- C twin of the Kāra
// ★ arm (binary search on the slope).
#include <stdio.h>
#include <stdint.h>

#define N 100000

static int64_t peak_index_in_mountain_array(const int64_t *arr, int64_t n) {
    int64_t lo = 0, hi = n - 1;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (arr[mid] < arr[mid + 1]) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 30000000, n = N;
    int64_t seed = 852;
    static int64_t arrays[64][N];
    for (int64_t g = 0; g < count; g++) {
        int64_t step = 1 + g % 10;
        int64_t peak = 1 + (next_random(&seed) * 32768 + next_random(&seed)) % (n - 2);
        int64_t v = 0, low = 0;
        for (int64_t i = 0; i < n; i++) {
            if (i > 0) {
                if (i <= peak) v += 1 + next_random(&seed) % step;
                else v -= 1 + next_random(&seed) % step;
            }
            arrays[g][i] = v;
            if (v < low) low = v;
        }
        for (int64_t i = 0; i < n; i++) arrays[g][i] -= low;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t p = peak_index_in_mountain_array(arrays[round % count], n);
        total += p;
        checksum = (checksum * 31 + p) % 1000000007;
    }
    printf("%lld rounds of %lld mountains: peaks sum to %lld, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)total, (long long)checksum);
    return 0;
}
