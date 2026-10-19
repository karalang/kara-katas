// LeetCode 803 -- Bricks Falling When Hit: the bench, mirroring
// hit_bricks.kara with the same union-find run backwards.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 803;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static const int64_t DR[4] = {-1, 1, 0, 0};
static const int64_t DC[4] = {0, 0, -1, 1};

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static void unite(int64_t *parent, int64_t *size, int64_t a, int64_t b) {
    int64_t ra = find(parent, a), rb = find(parent, b);
    if (ra == rb) {
        return;
    }
    if (size[ra] < size[rb]) {
        parent[ra] = rb;
        size[rb] += size[ra];
    } else {
        parent[rb] = ra;
        size[ra] += size[rb];
    }
}

// Join the brick at (r, c) to the roof if it is in the top row, and to
// each brick next to it.
static void join(int64_t r, int64_t c, int64_t rows, int64_t cols, int64_t **left, int64_t *parent,
                 int64_t *size) {
    int64_t here = r * cols + c;
    if (r == 0) {
        unite(parent, size, here, rows * cols);
    }
    for (int d = 0; d < 4; d++) {
        int64_t nr = r + DR[d], nc = c + DC[d];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && left[nr][nc] == 1) {
            unite(parent, size, here, nr * cols + nc);
        }
    }
}

static int64_t *hit_bricks(int64_t **grid, int64_t rows, int64_t cols, const int64_t (*hits)[2],
                           int64_t nhits) {
    int64_t **left = malloc((size_t)rows * sizeof(int64_t *));
    for (int64_t r = 0; r < rows; r++) {
        left[r] = malloc((size_t)cols * sizeof(int64_t));
        memcpy(left[r], grid[r], (size_t)cols * sizeof(int64_t));
    }
    for (int64_t k = 0; k < nhits; k++) {
        left[hits[k][0]][hits[k][1]] = 0;
    }
    int64_t roof = rows * cols;
    int64_t *parent = malloc((size_t)(roof + 1) * sizeof(int64_t));
    int64_t *size = malloc((size_t)(roof + 1) * sizeof(int64_t));
    for (int64_t i = 0; i < roof + 1; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            if (left[r][c] == 1) {
                join(r, c, rows, cols, left, parent, size);
            }
        }
    }
    int64_t *fallen = calloc((size_t)nhits, sizeof(int64_t));
    for (int64_t k = nhits - 1; k >= 0; k--) {
        int64_t r = hits[k][0], c = hits[k][1];
        if (grid[r][c] == 1) {
            int64_t before = size[find(parent, roof)];
            left[r][c] = 1;
            join(r, c, rows, cols, left, parent, size);
            int64_t after = size[find(parent, roof)];
            int64_t f = after - before - 1;
            fallen[k] = f > 0 ? f : 0;
        }
    }
    for (int64_t r = 0; r < rows; r++) {
        free(left[r]);
    }
    free(left);
    free(parent);
    free(size);
    return fallen;
}

// The wall with every brick that is not held up from the top row taken
// away, so that every brick starts held up.
static int64_t **settled(int64_t **grid, int64_t rows, int64_t cols) {
    int64_t **out = malloc((size_t)rows * sizeof(int64_t *));
    for (int64_t r = 0; r < rows; r++) {
        out[r] = calloc((size_t)cols, sizeof(int64_t));
    }
    int64_t *stack = malloc((size_t)(rows * cols) * 2 * sizeof(int64_t));
    int64_t top = 0;
    for (int64_t c = 0; c < cols; c++) {
        if (grid[0][c] == 1) {
            out[0][c] = 1;
            stack[top++] = 0;
            stack[top++] = c;
        }
    }
    while (top > 0) {
        int64_t c = stack[--top];
        int64_t r = stack[--top];
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + DR[d], nc = c + DC[d];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1 && out[nr][nc] == 0) {
                out[nr][nc] = 1;
                stack[top++] = nr;
                stack[top++] = nc;
            }
        }
    }
    free(stack);
    return out;
}

int main(void) {
    int64_t size = 200;
    int64_t **walls[8];
    static int64_t all_hits[8][20000][2];
    int64_t *cells = malloc((size_t)(size * size) * sizeof(int64_t));
    for (int w = 0; w < 8; w++) {
        int64_t **grid = malloc((size_t)size * sizeof(int64_t *));
        for (int64_t r = 0; r < size; r++) {
            grid[r] = malloc((size_t)size * sizeof(int64_t));
            for (int64_t c = 0; c < size; c++) {
                grid[r][c] = next_random() % 4 < 3 ? 1 : 0;
            }
        }
        walls[w] = settled(grid, size, size);
        for (int64_t r = 0; r < size; r++) {
            free(grid[r]);
        }
        free(grid);
        for (int64_t j = 0; j < size * size; j++) {
            cells[j] = j;
        }
        for (int64_t j = 1; j < size * size; j++) {
            int64_t t = next_random() % (j + 1);
            int64_t x = cells[j];
            cells[j] = cells[t];
            cells[t] = x;
        }
        for (int64_t j = 0; j < 20000; j++) {
            all_hits[w][j][0] = cells[j] / size;
            all_hits[w][j][1] = cells[j] % size;
        }
    }
    free(cells);
    int64_t rounds = 500;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t *fallen = hit_bricks(walls[r % 8], size, size, (const int64_t (*)[2])all_hits[r % 8], 20000);
        int64_t sum = 0;
        for (int64_t j = 0; j < 20000; j++) {
            sum += fallen[j];
        }
        total += sum;
        check = (check * 131 + sum + fallen[r % 20000]) % 1000000007;
        free(fallen);
    }
    printf("%lld rounds of 20000 hits: %lld bricks fell, checksum %lld\n", (long long)rounds, (long long)total,
           (long long)check);
    return 0;
}
