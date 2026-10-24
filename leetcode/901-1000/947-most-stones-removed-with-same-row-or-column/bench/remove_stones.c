// Benchmark: LeetCode #947 Most Stones Removed with Same Row or Column --
// the ★ arm, rows and columns joined, on sets of 1000 stones, LeetCode's
// largest. Mirrors remove_stones.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000
#define COUNT 20
#define LINES 20002

static int64_t find_line(int64_t *parent, int64_t v) {
    int64_t x = v;
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int64_t remove_stones(const int64_t (*stones)[2], int64_t n) {
    int64_t *parent = malloc(sizeof(int64_t) * LINES);
    for (int64_t v = 0; v < LINES; v++) parent[v] = -1;
    int64_t groups = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t row = stones[i][0];
        int64_t col = 10001 + stones[i][1];
        if (parent[row] < 0) {
            parent[row] = row;
            groups++;
        }
        if (parent[col] < 0) {
            parent[col] = col;
            groups++;
        }
        int64_t a = find_line(parent, row);
        int64_t b = find_line(parent, col);
        if (a != b) {
            parent[a] = b;
            groups--;
        }
    }
    free(parent);
    return n - groups;
}

static int64_t seed = 947;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t sets[COUNT][N][2];
static unsigned char taken[2000][2000];

int main(void) {
    const int64_t rounds = 1000, count = COUNT, n = N;
    for (int64_t c = 0; c < count; c++) {
        int64_t side = 200 + next_random() % 1801;
        int64_t placed = 0;
        while (placed < n) {
            int64_t x = next_random() % side;
            int64_t y = next_random() % side;
            if (!taken[x][y]) {
                taken[x][y] = 1;
                sets[c][placed][0] = x;
                sets[c][placed][1] = y;
                placed++;
            }
        }
        for (int64_t i = 0; i < n; i++) taken[sets[c][i][0]][sets[c][i][1]] = 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t m = remove_stones((const int64_t (*)[2])sets[(r + i) % count], n);
            total += m;
            check = (check * 1000003 + m) % 1000000007;
        }
    }
    printf("%lld rounds over %lld sets of %lld stones: %lld removed, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    return 0;
}
