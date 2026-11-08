// LeetCode #2017: Grid Game -- the ★ arm's benchmark, a mirror of grid.kara.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

enum { GRIDS = 200, N = 50000 };

static int64_t grid_game(const int64_t *upper, const int64_t *lower, int n) {
    int64_t top = 0, bottom = 0, best = INT64_MAX;
    for (int i = 0; i < n; i++) top += upper[i];
    for (int i = 0; i < n; i++) {
        top -= upper[i];
        int64_t share = top > bottom ? top : bottom;
        if (share < best) best = share;
        bottom += lower[i];
    }
    return best;
}

static int64_t seed = 2017;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *cells = malloc((size_t)GRIDS * 2 * N * sizeof(int64_t));
    for (size_t k = 0; k < (size_t)GRIDS * 2 * N; k++) cells[k] = next_random() * 3 % 100000 + 1;
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 10; r++) {
        for (int g = 0; g < GRIDS; g++) {
            const int64_t *upper = cells + (size_t)g * 2 * N;
            int64_t answer = grid_game(upper, upper + N, N);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    free(cells);
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
