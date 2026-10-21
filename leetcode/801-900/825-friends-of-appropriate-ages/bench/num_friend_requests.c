// Benchmark for #825: Friends Of Appropriate Ages -- the ★ arm (counts by age).
//
// Mirrors num_friend_requests.kara: the people counted by age once, and
// every pair of ages tested with the statement's three conditions, each
// pair that passes adding one request from every person of the first age
// to every person of the second, but for a person and themself. The
// counts are a fresh array each call, as the Kāra program's Vec is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int asks(int64_t x, int64_t y) { return !(2 * y <= x + 14 || y > x || (y > 100 && x < 100)); }

static int64_t num_friend_requests(const int64_t *ages, int64_t n) {
    int64_t *count = calloc(121, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[ages[i]]++;
    int64_t requests = 0;
    for (int64_t x = 1; x < 121; x++) {
        if (count[x] == 0) continue;
        for (int64_t y = 1; y < 121; y++) {
            if (count[y] > 0 && asks(x, y)) {
                requests += count[x] * count[y];
                if (x == y) requests -= count[x];
            }
        }
    }
    free(count);
    return requests;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 64;
    int64_t rounds = 50000;
    int64_t seed = 825;
    int64_t *lists[64];
    for (int64_t g = 0; g < count; g++) {
        lists[g] = malloc(20000 * sizeof(int64_t));
        for (int64_t i = 0; i < 20000; i++) lists[g][i] = 1 + next_random(&seed) % 120;
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t r = num_friend_requests(lists[round % count], 20000);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    printf("%lld rounds of %lld lists: total %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
