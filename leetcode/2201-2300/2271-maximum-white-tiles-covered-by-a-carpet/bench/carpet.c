// LeetCode #2271: Maximum White Tiles Covered by a Carpet -- the bench,
// the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t l, r; } Tile;

static int by_tile(const void *a, const void *b) {
    const Tile *x = a, *y = b;
    if (x->l != y->l) return (x->l > y->l) - (x->l < y->l);
    return (x->r > y->r) - (x->r < y->r);
}

static int64_t maximum_white_tiles(const Tile *tiles, int64_t m, int64_t carpet_len) {
    Tile *s = malloc(m * sizeof(Tile));
    memcpy(s, tiles, m * sizeof(Tile));
    qsort(s, m, sizeof(Tile), by_tile);
    int64_t best = 0, whole = 0, j = 0;
    for (int64_t i = 0; i < m; i++) {
        int64_t end = s[i].l + carpet_len - 1;
        while (j < m && s[j].r <= end) {
            whole += s[j].r - s[j].l + 1;
            j++;
        }
        int64_t part = (j < m && s[j].l <= end) ? end - s[j].l + 1 : 0;
        if (whole + part > best) best = whole + part;
        if (j > i) whole -= s[i].r - s[i].l + 1;
        else j = i + 1;
    }
    free(s);
    return best;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2271;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t lens[] = {1000, 1000000, 1000000000};
    Tile *tiles = malloc(50000 * sizeof(Tile));
    int64_t check = 0;
    for (int t = 0; t < 30; t++) {
        int64_t at = 1;
        for (int i = 0; i < 50000; i++) {
            at += next_random() % 10001;
            int64_t end = at + next_random() % 10000;
            tiles[i].l = at;
            tiles[i].r = end;
            at = end + 1;
        }
        for (int64_t i = 49999; i >= 1; i--) {
            int64_t k = next_random() % (i + 1);
            Tile x = tiles[i];
            tiles[i] = tiles[k];
            tiles[k] = x;
        }
        check = (check * 31 + maximum_white_tiles(tiles, 50000, lens[t % 3])) % 1000000007;
    }
    free(tiles);
    printf("30 sets of 5 * 10^4: checksum %lld\n", (long long)check);
    return 0;
}
