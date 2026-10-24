// Benchmark: LeetCode #939 Minimum Area Rectangle -- the ★ arm, pairs as
// diagonals, on 20 sets of 500 points, LeetCode's most, in 10 rounds.
// Mirrors min_area_rect.kara, .rs, .py and go-seq/. The set is a table
// of 1024 slots with linear probing.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define SLOTS 1024

static int64_t table[SLOTS];
static unsigned char used[SLOTS];

static uint64_t slot_of(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    return (h >> 54) & (SLOTS - 1);
}

static void insert(int64_t key) {
    uint64_t s = slot_of(key);
    while (used[s] && table[s] != key) s = (s + 1) & (SLOTS - 1);
    used[s] = 1;
    table[s] = key;
}

static int contains(int64_t key) {
    uint64_t s = slot_of(key);
    while (used[s]) {
        if (table[s] == key) return 1;
        s = (s + 1) & (SLOTS - 1);
    }
    return 0;
}

static int64_t llabs64(int64_t v) { return v < 0 ? -v : v; }

static int64_t min_area_rect(const int64_t (*points)[2], int n) {
    memset(used, 0, sizeof used);
    for (int i = 0; i < n; i++) insert(points[i][0] * 40001 + points[i][1]);
    int64_t best = 0;
    for (int i = 0; i < n; i++) {
        int64_t x1 = points[i][0], y1 = points[i][1];
        for (int j = i + 1; j < n; j++) {
            int64_t x2 = points[j][0], y2 = points[j][1];
            if (x1 != x2 && y1 != y2 && contains(x1 * 40001 + y2) && contains(x2 * 40001 + y1)) {
                int64_t area = llabs64(x1 - x2) * llabs64(y1 - y2);
                if (best == 0 || area < best) best = area;
            }
        }
    }
    return best;
}

static int64_t seed = 939;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t sets[20][500][2];

int main(void) {
    int rounds = 10, count = 20;
    for (int s = 0; s < count; s++) {
        int64_t step = 1 + next_random() % 100;
        int64_t ox = next_random() % 1000;
        int64_t oy = next_random() % 1000;
        unsigned char taken[1600] = {0};
        int n = 0;
        while (n < 500) {
            int64_t hi = next_random();
            int64_t c = (hi * 32768 + next_random()) % 1600;
            if (!taken[c]) {
                taken[c] = 1;
                sets[s][n][0] = ox + (c % 40) * step;
                sets[s][n][1] = oy + (c / 40) * step;
                n++;
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            int64_t a = min_area_rect((const int64_t (*)[2])sets[(r + i) % count], 500);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%d rounds over %d sets of 500 points: areas adding to %lld, checksum %lld\n", rounds, count,
           (long long)total, (long long)check);
    return 0;
}
