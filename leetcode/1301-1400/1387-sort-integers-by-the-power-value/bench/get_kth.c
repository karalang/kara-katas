// LeetCode #1387 bench -- C: the ★ arm: each value walked only until it
// meets one whose power is known, in an open-addressing hash table that
// every walk fills on its way back; the (power, value) pairs sorted with
// qsort and the k-th read off.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 16384

static int64_t keys[SLOTS];
static int vals[SLOTS];
static unsigned char used[SLOTS];
static int64_t path[1024];
static int64_t keyed[1000];

static unsigned slot_of(int64_t v) {
    unsigned h = (unsigned)((uint64_t)v * 11400714819323198485ull >> 50);
    while (used[h] && keys[h] != v) h = (h + 1) & (SLOTS - 1);
    return h;
}

static int by_key(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int get_kth(int lo, int hi, int k) {
    memset(used, 0, sizeof used);
    unsigned h = slot_of(1);
    used[h] = 1, keys[h] = 1, vals[h] = 0;
    int m = 0;
    for (int x = lo; x <= hi; x++) {
        int len = 0;
        int64_t v = x;
        for (;;) {
            h = slot_of(v);
            if (used[h]) break;
            path[len++] = v;
            v = v % 2 == 0 ? v / 2 : 3 * v + 1;
        }
        int steps = vals[h];
        while (len > 0) {
            int64_t p = path[--len];
            steps++;
            unsigned s = slot_of(p);
            used[s] = 1, keys[s] = p, vals[s] = steps;
        }
        // (power, value) packed so that the order is the pair's
        keyed[m++] = (int64_t)vals[slot_of(x)] << 32 | x;
    }
    qsort(keyed, m, sizeof(int64_t), by_key);
    return (int)(keyed[k - 1] & 0xffffffff);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1387;
    int64_t check = 0;
    for (int q = 0; q < 4000; q++) {
        seed = (seed + check) % 2147483648LL;
        int64_t lo = 1 + next_random(&seed) % 200;
        int64_t hi = 800 + next_random(&seed) % 201;
        int64_t k = 1 + next_random(&seed) % (hi - lo + 1);
        check = (check * 131 + get_kth((int)lo, (int)hi, (int)k)) % 1000000007;
    }
    printf("4000 queries over ranges up to 1 to 1000: checksum %lld\n", (long long)check);
    return 0;
}
