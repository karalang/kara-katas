// Benchmark: LeetCode #1095 Find in Mountain Array -- C mirror of
// find_in_mountain_array.kara: the ★ arm's three binary searches through a
// counted `get` (an atomic counter, as Kāra's `Atomic[i64]`), over 64
// mountains of 10^4 values built once, 100 rounds of 64 targets each.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int32_t *values;
    int32_t len;
    int64_t calls;
} MountainArray;

static int32_t get(MountainArray *m, int32_t index) {
    __atomic_fetch_add(&m->calls, 1, __ATOMIC_SEQ_CST);
    return m->values[index];
}

static int32_t length(MountainArray *m) { return m->len; }

static int32_t find_in_mountain_array(int32_t target, MountainArray *mountain) {
    int32_t n = length(mountain);
    int32_t lo = 0, hi = n - 1;
    while (lo < hi) {
        int32_t mid = (lo + hi) / 2;
        if (get(mountain, mid) < get(mountain, mid + 1)) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    int32_t peak = lo;
    lo = 0;
    hi = peak;
    while (lo <= hi) {
        int32_t mid = (lo + hi) / 2;
        int32_t v = get(mountain, mid);
        if (v == target) return mid;
        if (v < target) lo = mid + 1; else hi = mid - 1;
    }
    lo = peak + 1;
    hi = n - 1;
    while (lo <= hi) {
        int32_t mid = (lo + hi) / 2;
        int32_t v = get(mountain, mid);
        if (v == target) return mid;
        if (v > target) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}

static int64_t seed = 1095;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    MountainArray mountains[64];
    for (int64_t j = 0; j < 64; j++) {
        int64_t up = 1 + j * 9997 / 63;
        int64_t down = 9999 - up;
        int32_t *v = malloc(10000 * sizeof(int32_t));
        int32_t len = 0;
        v[len++] = (int32_t)(down * 50000 + next_random() % 20);
        for (int64_t i = 0; i < up; i++) {
            int32_t last = v[len - 1];
            v[len++] = last + 1 + (int32_t)(next_random() % 50000);
        }
        for (int64_t i = 0; i < down; i++) {
            int32_t last = v[len - 1];
            v[len++] = last - 1 - (int32_t)(next_random() % 50000);
        }
        mountains[j].values = v;
        mountains[j].len = len;
        mountains[j].calls = 0;
    }
    int64_t found = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int j = 0; j < 64; j++) {
            MountainArray *m = &mountains[j];
            for (int64_t q = 0; q < 64; q++) {
                int64_t k = (round * 7919 + q * 104729) % 10000;
                int32_t target = m->values[k] + (int32_t)((round + q) % 3) - 1;
                int32_t at = find_in_mountain_array(target, m);
                if (at >= 0) found++;
                check = (check * 31 + at + 1) % 1000000007;
            }
        }
    }
    int64_t calls = 0;
    for (int j = 0; j < 64; j++) {
        calls += __atomic_load_n(&mountains[j].calls, __ATOMIC_SEQ_CST);
        free(mountains[j].values);
    }
    printf("100 rounds over 64 mountains of 10^4 values: %lld of 409600 found, %lld calls of get, checksum %lld\n",
           (long long)found, (long long)calls, (long long)check);
    return 0;
}
