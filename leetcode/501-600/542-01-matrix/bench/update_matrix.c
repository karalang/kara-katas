// Benchmark for #542: C mirror of the ★ arm (breadth-first search from
// every 0 at once); see update_matrix.kara. The grid is a flat array of
// rows; the queue is a ring of cell indexes as large as the grid.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *update_matrix(const int64_t *mat, int64_t m, int64_t n) {
    int64_t *dist = malloc(m * n * sizeof(int64_t));
    int64_t *queue = malloc(m * n * sizeof(int64_t));
    int64_t head = 0, tail = 0;
    for (int64_t i = 0; i < m * n; i++) {
        if (mat[i] == 0) {
            dist[i] = 0;
            queue[tail++] = i;
        } else {
            dist[i] = -1;
        }
    }
    static const int64_t steps[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    while (head < tail) {
        int64_t cell = queue[head++];
        int64_t r = cell / n, c = cell % n;
        for (int s = 0; s < 4; s++) {
            int64_t nr = r + steps[s][0], nc = c + steps[s][1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && dist[nr * n + nc] < 0) {
                dist[nr * n + nc] = dist[cell] + 1;
                queue[tail++] = nr * n + nc;
            }
        }
    }
    free(queue);
    return dist;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 20 random 100 by 100 grids (the problem's 10,000 cells), from half
    // ones to 88 in a hundred, built once. Then 50 times over every grid
    // is answered; one row of the answer, picked by the round and the
    // grid, is summed, and one cell goes into the checksum.
    int64_t grids = 20, seed = 542;
    int64_t *all = malloc(grids * 10000 * sizeof(int64_t));
    for (int64_t g = 0; g < grids; g++) {
        int64_t ones = 50 + 2 * g;
        for (int i = 0; i < 10000; i++) all[g * 10000 + i] = next_random(&seed) % 100 < ones ? 1 : 0;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < 50; r++) {
        for (int64_t t = 0; t < grids; t++) {
            int64_t *answer = update_matrix(all + t * 10000, 100, 100);
            int64_t row = (r * 7 + t * 13) % 100;
            for (int c = 0; c < 100; c++) total += answer[row * 100 + c];
            int64_t cell = answer[((r * 11 + t * 3) % 100) * 100 + (r * 5 + t * 17) % 100];
            checksum = (checksum * 31 + cell) % 1000000007;
            free(answer);
        }
    }
    printf("%lld grids, 50 times each: row sum %lld, checksum %lld\n", (long long)grids,
           (long long)total, (long long)checksum);
    return 0;
}
