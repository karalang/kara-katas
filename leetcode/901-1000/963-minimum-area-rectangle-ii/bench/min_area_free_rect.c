// Benchmark: LeetCode #963 Minimum Area Rectangle II -- the ★ arm,
// diagonals grouped by centre, on 50 points, LeetCode's largest, packed
// into small grids so that many pairs share a centre and a length. Each
// call first moves one point to a free spot. Mirrors
// min_area_free_rect.kara, .rs, .py and go-seq/. The map is an
// open-addressing table of 4096 slots on the stack, each holding a key
// and the head of a list of that key's pairs.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define N 50
#define COUNT 50
#define SLOTS 4096
#define PAIRS (N * (N - 1) / 2)

static int64_t seed = 963;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static double min_area_free_rect(int64_t points[][2], int n) {
    int64_t keys[SLOTS][3];
    int head[SLOTS];
    int pi[PAIRS], pj[PAIRS], next[PAIRS];
    memset(head, -1, sizeof head);
    int count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int64_t dx = points[i][0] - points[j][0], dy = points[i][1] - points[j][1];
            int64_t k0 = points[i][0] + points[j][0], k1 = points[i][1] + points[j][1], k2 = dx * dx + dy * dy;
            uint64_t h = ((uint64_t)k0 * 0x9E3779B97F4A7C15ULL) ^ ((uint64_t)k1 * 0xC2B2AE3D27D4EB4FULL) ^
                         ((uint64_t)k2 * 0x165667B19E3779F9ULL);
            int s = (int)((h >> 40) & (SLOTS - 1));
            while (head[s] != -1 && (keys[s][0] != k0 || keys[s][1] != k1 || keys[s][2] != k2)) s = (s + 1) & (SLOTS - 1);
            if (head[s] == -1) {
                keys[s][0] = k0;
                keys[s][1] = k1;
                keys[s][2] = k2;
            }
            pi[count] = i;
            pj[count] = j;
            next[count] = head[s];
            head[s] = count++;
        }
    }
    int64_t best = 0;
    for (int s = 0; s < SLOTS; s++) {
        for (int x = head[s]; x != -1; x = next[x]) {
            for (int y = next[x]; y != -1; y = next[y]) {
                int i = pi[x], k = pi[y], l = pj[y];
                int64_t ux = points[k][0] - points[i][0], uy = points[k][1] - points[i][1];
                int64_t vx = points[l][0] - points[i][0], vy = points[l][1] - points[i][1];
                int64_t area = ux * vy - uy * vx;
                if (area < 0) area = -area;
                if (best == 0 || area < best) best = area;
            }
        }
    }
    return (double)best;
}

static int has(int64_t points[][2], int n, int64_t x, int64_t y) {
    for (int i = 0; i < n; i++)
        if (points[i][0] == x && points[i][1] == y) return 1;
    return 0;
}

static int64_t cases[COUNT][N][2];

int main(void) {
    int rounds = 40;
    for (int i = 0; i < COUNT; i++) {
        int64_t top = 7 + i % 10;
        int len = 0;
        while (len < N) {
            int64_t x = next_random() % (top + 1), y = next_random() % (top + 1);
            if (!has(cases[i], len, x, y)) {
                cases[i][len][0] = x;
                cases[i][len][1] = y;
                len++;
            }
        }
    }
    double total = 0.0;
    int64_t check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            int c = (r + i) % COUNT;
            int64_t top = 7 + c % 10;
            int64_t p = next_random() % N;
            int64_t x = next_random() % (top + 1), y = next_random() % (top + 1);
            if (!has(cases[c], N, x, y)) {
                cases[c][p][0] = x;
                cases[c][p][1] = y;
            }
            double a = min_area_free_rect(cases[c], N);
            total += a;
            check = (check * 31 + (int64_t)a + i) % 1000000007;
        }
    }
    printf("%d rounds over 50 cases of 50 points: the areas sum to %.5f, checksum %lld\n", rounds, total,
           (long long)check);
    return 0;
}
