// Bench mirror of snake_game.kara (the grid + ring-buffer arm), same algorithm.
// A byte per cell says which cells are body; the body is a ring buffer of cell
// indices as large as the board.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ROUNDS 30
#define WIDTH 1000
#define HEIGHT 400

typedef struct {
    int64_t width, height;
    int64_t *food_r, *food_c;
    int64_t food_len, next_food;
    int64_t *ring;
    int64_t cap, start, len;
    uint8_t *covered;
} SnakeGame;

static int64_t step(SnakeGame *g, char dir) {
    int64_t head = g->ring[(g->start + g->len - 1) % g->cap];
    int64_t r = head / g->width, c = head % g->width;
    int64_t nr = r, nc = c;
    if (dir == 'U') nr--;
    else if (dir == 'D') nr++;
    else if (dir == 'L') nc--;
    else nc++;
    if (nr < 0 || nr >= g->height || nc < 0 || nc >= g->width) return -1;
    int64_t cell = nr * g->width + nc;
    if (g->next_food < g->food_len && g->food_r[g->next_food] == nr && g->food_c[g->next_food] == nc) {
        g->next_food++;
    } else {
        g->covered[g->ring[g->start]] = 0;
        g->start = (g->start + 1) % g->cap;
        g->len--;
    }
    if (g->covered[cell]) return -1;
    g->ring[(g->start + g->len) % g->cap] = cell;
    g->len++;
    g->covered[cell] = 1;
    return g->next_food;
}

int main(void) {
    int64_t sink = 0;
    for (int64_t round = 0; round < ROUNDS; round++) {
        int64_t w = WIDTH, h = HEIGHT + 2 * round, n = w * h;
        char *moves = malloc((size_t)n);
        int64_t m = 0;
        for (int64_t i = 0; i < w - 1; i++) moves[m++] = 'R';
        for (int64_t row = 1; row < h; row++) {
            moves[m++] = 'D';
            char d = row % 2 == 1 ? 'L' : 'R';
            for (int64_t i = 0; i < w - 2; i++) moves[m++] = d;
        }
        moves[m++] = 'L';
        for (int64_t i = 0; i < h - 1; i++) moves[m++] = 'U';

        int64_t want = n / 4;
        int64_t *fr = malloc(sizeof(int64_t) * (size_t)want);
        int64_t *fc = malloc(sizeof(int64_t) * (size_t)want);
        int64_t nf = 0, r = 0, c = 0, t = 0;
        while (nf < want) {
            char d = moves[t];
            if (d == 'U') r--;
            else if (d == 'D') r++;
            else if (d == 'L') c--;
            else c++;
            if (t % 3 == 2) {
                fr[nf] = r;
                fc[nf] = c;
                nf++;
            }
            t++;
        }
        SnakeGame g = {w, h, fr, fc, nf, 0, calloc((size_t)n, sizeof(int64_t)), n, 0, 1, calloc((size_t)n, 1)};
        g.covered[0] = 1;
        for (int64_t t2 = 0; t2 < 3 * n; t2++) {
            int64_t s = step(&g, moves[t2 % n]);
            sink = (sink * 31 + s + t2) % 1000000007;
        }
        sink = (sink + g.len) % 1000000007;
        free(g.ring);
        free(g.covered);
        free(fr);
        free(fc);
        free(moves);
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
