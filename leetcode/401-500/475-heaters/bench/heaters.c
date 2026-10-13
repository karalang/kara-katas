// Benchmark for #475: C mirror of the ★ arm (sort the heaters, binary
// search per house); see heaters.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t first_at_or_after(const int64_t *heaters, int64_t len, int64_t x) {
    int64_t lo = 0;
    int64_t hi = len;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (heaters[mid] < x) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

static int cmp_asc(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t find_radius(const int64_t *houses, int64_t nh, const int64_t *heaters, int64_t nw) {
    int64_t *sorted = malloc(sizeof(int64_t) * (size_t)nw);
    memcpy(sorted, heaters, sizeof(int64_t) * (size_t)nw);
    qsort(sorted, (size_t)nw, sizeof(int64_t), cmp_asc);
    int64_t radius = 0;
    for (int64_t k = 0; k < nh; k++) {
        int64_t house = houses[k];
        int64_t at = first_at_or_after(sorted, nw, house);
        int64_t nearest = INT64_MAX;
        if (at < nw) {
            nearest = sorted[at] - house;
        }
        if (at > 0 && house - sorted[at - 1] < nearest) {
            nearest = house - sorted[at - 1];
        }
        if (nearest > radius) {
            radius = nearest;
        }
    }
    free(sorted);
    return radius;
}

static int64_t seed = 475;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int64_t houses[30000];
    static int64_t heaters[30000];
    for (int i = 0; i < 30000; i++) {
        int64_t a = next_random();
        int64_t b = next_random();
        houses[i] = 1 + (a * 32768 + b) % 1000000000;
    }
    int rounds = 200;
    int64_t total = 0;
    int64_t checksum = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 30000; i++) {
            int64_t a = next_random();
            int64_t b = next_random();
            heaters[i] = 1 + (a * 32768 + b) % 1000000000;
        }
        int64_t got = find_radius(houses, 30000, heaters, 30000);
        total += got;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%d rounds of 30000 houses and 30000 heaters: radii add up to %lld, checksum %lld\n", rounds, (long long)total, (long long)checksum);
    return 0;
}
