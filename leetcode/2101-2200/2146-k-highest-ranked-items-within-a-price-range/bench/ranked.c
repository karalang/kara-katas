// LeetCode #2146: K Highest Ranked Items Within a Price Range -- the
// benchmark, the same algorithm as ranked.kara: a breadth-first search
// over an array queue, then `qsort` of the rank tuples (no two tuples
// are equal, so the sort's instability cannot show).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define S 316

typedef struct { int64_t dist, price, r, c; } Item;

static int by_rank(const void *x, const void *y) {
    const Item *a = x, *b = y;
    if (a->dist != b->dist) return a->dist < b->dist ? -1 : 1;
    if (a->price != b->price) return a->price < b->price ? -1 : 1;
    if (a->r != b->r) return a->r < b->r ? -1 : 1;
    if (a->c != b->c) return a->c < b->c ? -1 : 1;
    return 0;
}

static int64_t queue[S * S][3];
static Item found[S * S];
static char seen[S][S];

static int64_t highest_ranked_k_items(int64_t grid[S][S], int64_t low, int64_t high, int64_t sr, int64_t sc, int64_t k, int64_t out[][2]) {
    memset(seen, 0, sizeof seen);
    seen[sr][sc] = 1;
    int64_t head = 0, tail = 0, nfound = 0;
    queue[tail][0] = sr; queue[tail][1] = sc; queue[tail][2] = 0; tail++;
    static const int64_t dirs[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    while (head < tail) {
        int64_t r = queue[head][0], c = queue[head][1], dist = queue[head][2];
        head++;
        int64_t price = grid[r][c];
        if (price >= low && price <= high) {
            found[nfound].dist = dist; found[nfound].price = price;
            found[nfound].r = r; found[nfound].c = c; nfound++;
        }
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + dirs[d][0], nc = c + dirs[d][1];
            if (nr >= 0 && nr < S && nc >= 0 && nc < S && !seen[nr][nc] && grid[nr][nc] != 0) {
                seen[nr][nc] = 1;
                queue[tail][0] = nr; queue[tail][1] = nc; queue[tail][2] = dist + 1; tail++;
            }
        }
    }
    qsort(found, nfound, sizeof(Item), by_rank);
    int64_t taken = nfound < k ? nfound : k;
    for (int64_t i = 0; i < taken; i++) { out[i][0] = found[i].r; out[i][1] = found[i].c; }
    return taken;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t draw(int64_t *seed) {
    if (next_random(seed) % 5 == 0) return 0;
    return next_random(seed) % 99999 + 2;
}

static int64_t grids[4][S][S];
static int64_t cells[1000][2];

int main(void) {
    int64_t seed = 2146;
    for (int g = 0; g < 4; g++)
        for (int r = 0; r < S; r++)
            for (int c = 0; c < S; c++) grids[g][r][c] = draw(&seed);
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int g = 0; g < 4; g++) {
            int64_t r = next_random(&seed) % S;
            int64_t c = next_random(&seed) % S;
            grids[g][r][c] = draw(&seed);
            int64_t sr = next_random(&seed) % S;
            int64_t sc = next_random(&seed) % S;
            if (grids[g][sr][sc] == 0) grids[g][sr][sc] = 1;
            int64_t got = highest_ranked_k_items(grids[g], 2, 50000, sr, sc, 1000, cells);
            total += got;
            for (int64_t i = 0; i < got; i++) check = (check * 31 + cells[i][0] * 1000 + cells[i][1] + round) % 1000000007;
        }
    }
    printf("100 searches: %lld items in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
