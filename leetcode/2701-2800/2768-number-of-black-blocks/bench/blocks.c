// LeetCode #2768: Number of Black Blocks -- the bench (blocks.kara in C):
// the blocks in a hash map keyed by the top-left corner, open addressing
// with linear probing, each black cell counted into every block it lies
// in; the slots used are kept in a list, read for the counts and cleared
// after each grid.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BITS 17
#define CAP (1 << BITS)
#define CELLS 10000
#define COUNT 100

static int64_t seed = 2768;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static uint64_t hash(int64_t x, int64_t y) {
    uint64_t z = (uint64_t)x * 0x9e3779b97f4a7c15ULL + (uint64_t)y;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return (z ^ (z >> 31)) >> (64 - BITS);
}

static int64_t key_x[CAP], key_y[CAP], value[CAP];
static uint32_t used[4 * CELLS];

static int64_t imin(int64_t a, int64_t b) { return a < b ? a : b; }
static int64_t imax(int64_t a, int64_t b) { return a > b ? a : b; }

// an empty slot holds a count of 0
static void count_black_blocks(int64_t m, int64_t n, const int64_t *cells, int64_t c, int64_t *counts) {
    int64_t size = 0;
    for (int64_t k = 0; k < c; k++) {
        int64_t x = cells[2 * k], y = cells[2 * k + 1];
        for (int64_t bx = imax(x - 1, 0); bx <= imin(x, m - 2); bx++) {
            for (int64_t by = imax(y - 1, 0); by <= imin(y, n - 2); by++) {
                uint64_t i = hash(bx, by);
                while (value[i] != 0 && (key_x[i] != bx || key_y[i] != by)) {
                    i = (i + 1) & (CAP - 1);
                }
                if (value[i] == 0) {
                    key_x[i] = bx;
                    key_y[i] = by;
                    used[size++] = (uint32_t)i;
                }
                value[i] += 1;
            }
        }
    }
    for (int i = 0; i < 5; i++) counts[i] = 0;
    for (int64_t k = 0; k < size; k++) {
        counts[value[used[k]]] += 1;
        value[used[k]] = 0;
    }
    counts[0] = (m - 1) * (n - 1) - size;
}

static int64_t gm[COUNT], gn[COUNT];
static int64_t cells[COUNT][2 * CELLS];

int main(void) {
    int rounds = 5;
    for (int g = 0; g < COUNT; g++) {
        int64_t side = wide() % 900 + 101;
        int64_t area = side * side;
        int64_t m = side + wide() % (100001 - side);
        int64_t n = side + wide() % (100001 - side);
        int64_t x0 = wide() % (m - side + 1);
        int64_t y0 = wide() % (n - side + 1);
        int64_t stride = wide() % area;
        while (gcd(stride, area) != 1) stride = wide() % area;
        int64_t start = wide() % area;
        for (int64_t k = 0; k < CELLS; k++) {
            int64_t at = (start + k * stride) % area;
            cells[g][2 * k] = x0 + at / side;
            cells[g][2 * k + 1] = y0 + at % side;
        }
        gm[g] = m;
        gn[g] = n;
    }
    int64_t sums[5] = {0, 0, 0, 0, 0};
    int64_t check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int g = 0; g < COUNT; g++) {
            int64_t counts[5];
            count_black_blocks(gm[g], gn[g], cells[g], CELLS, counts);
            for (int i = 0; i < 5; i++) {
                sums[i] += counts[i];
                check = (check * 31 + counts[i] % 1000000007 + r + 1) % 1000000007;
            }
        }
    }
    printf("%d grids of 10^4 cells, %d rounds: counts sum to [%lld, %lld, %lld, %lld, %lld], checksum %lld\n", COUNT, rounds,
           (long long)sums[0], (long long)sums[1], (long long)sums[2], (long long)sums[3], (long long)sums[4], (long long)check);
    return 0;
}
