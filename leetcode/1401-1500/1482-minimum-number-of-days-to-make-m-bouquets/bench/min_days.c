// LeetCode #1482: Minimum Number of Days to Make m Bouquets -- bench, the
// C twin of min_days.kara.
#include <stdint.h>
#include <stdio.h>

#define N 100000

static int64_t bouquets(const int32_t *bloom_day, int n, int32_t k, int32_t day) {
    int64_t made = 0;
    int32_t run = 0;
    for (int i = 0; i < n; i++) {
        if (bloom_day[i] <= day) {
            run += 1;
            if (run == k) {
                made += 1;
                run = 0;
            }
        } else {
            run = 0;
        }
    }
    return made;
}

static int32_t min_days(const int32_t *bloom_day, int n, int32_t m, int32_t k) {
    if ((int64_t)m * (int64_t)k > n) return -1;
    int32_t lo = bloom_day[0], hi = bloom_day[0];
    for (int i = 1; i < n; i++) {
        if (bloom_day[i] < lo) lo = bloom_day[i];
        if (bloom_day[i] > hi) hi = bloom_day[i];
    }
    while (lo < hi) {
        int32_t mid = lo + (hi - lo) / 2;
        if (bouquets(bloom_day, n, k, mid) >= m) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int32_t bloom[N];

int main(void) {
    int64_t seed = 1482;
    for (int i = 0; i < N; i++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        bloom[i] = (int32_t)(1 + (hi * 32768 + lo) % 1000000000);
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 150; pass++) {
        bloom[check % N] = (int32_t)(1 + (check * 7) % 1000000000);
        int64_t k = 1 + check % 10;
        int64_t m = 1 + (check / 10) % (N / k + 100);
        check = (check * 31 + min_days(bloom, N, (int32_t)m, (int32_t)k) + 1 + pass) % 1000000007;
    }
    printf("150 passes over 100000 flowers: checksum %lld\n", (long long)check);
    return 0;
}
