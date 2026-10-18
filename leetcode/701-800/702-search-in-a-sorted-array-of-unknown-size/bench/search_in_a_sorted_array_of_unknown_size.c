// LeetCode #702: Search in a Sorted Array of Unknown Size -- bench program, C mirror of the doubling arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *secret;
    int64_t len;
    int64_t reads;
} ArrayReader;

static int64_t get(ArrayReader *r, int64_t index) {
    r->reads += 1;
    if (index < 0 || index >= r->len) {
        return 2147483647;
    }
    return r->secret[index];
}

static int64_t search(ArrayReader *reader, int64_t target) {
    int64_t lo = 0;
    int64_t hi = 1;
    while (get(reader, hi) < target) {
        lo = hi;
        hi *= 2;
    }
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        int64_t v = get(reader, mid);
        if (v == target) {
            return mid;
        }
        if (v < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 702;
    ArrayReader readers[100];
    for (int a = 0; a < 100; a++) {
        int64_t *secret = malloc(10000 * sizeof(int64_t));
        int64_t v = -10000;
        for (int i = 0; i < 10000; i++) {
            secret[i] = v;
            v += 1 + next_random(&seed) % 2;
        }
        readers[a] = (ArrayReader){secret, 10000, 0};
    }
    const int rounds = 5;
    int64_t found = 0;
    int64_t checksum = 0;
    for (int round = 0; round < rounds; round++) {
        for (int a = 0; a < 100; a++) {
            for (int64_t target = -10000; target <= 10000; target += 2) {
                int64_t at = search(&readers[a], target);
                if (at >= 0) {
                    found += 1;
                    checksum = (checksum * 31 + at) % 1000000007;
                }
            }
        }
    }
    int64_t reads = 0;
    for (int a = 0; a < 100; a++) {
        reads += readers[a].reads;
        free(readers[a].secret);
    }
    printf("%d rounds of 100 arrays of 10000: %lld found, %lld reads, checksum %lld\n", rounds,
           (long long)found, (long long)reads, (long long)checksum);
    return 0;
}
