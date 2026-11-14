// LeetCode #1559: Detect Cycles in 2D Grid -- bench: the ★ arm (a search
// on a stack, each cell with the cell it came from) over 20 comb grids of
// 500 by 500 with no cycle, half with two cells made `a` to join two teeth
// in one, built once, each asked 5 times.
// C mirror of cycles.kara; a grid is one block of 32-bit letters, as wide as a char.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 500

static int contains_cycle(const uint32_t *grid, int64_t rows, int64_t cols) {
    char *seen = calloc(rows * cols, 1);
    int64_t cap = 16, len = 0;
    int64_t *stack = malloc(cap * 2 * sizeof(int64_t));
    static const int64_t dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};
    int found = 0;
    for (int64_t start = 0; start < rows * cols && !found; start++) {
        if (seen[start]) continue;
        seen[start] = 1;
        len = 0;
        stack[0] = start;
        stack[1] = -1;
        len = 1;
        while (len > 0 && !found) {
            len--;
            int64_t cell = stack[2 * len], from = stack[2 * len + 1];
            int64_t r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int64_t nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr * cols + nc] != grid[r * cols + c])
                    continue;
                int64_t next = nr * cols + nc;
                if (next == from) continue;
                if (seen[next]) {
                    found = 1;
                    break;
                }
                seen[next] = 1;
                if (len == cap) {
                    cap *= 2;
                    stack = realloc(stack, cap * 2 * sizeof(int64_t));
                }
                stack[2 * len] = next;
                stack[2 * len + 1] = cell;
                len++;
            }
        }
    }
    free(seen);
    free(stack);
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1559;
    static uint32_t *grids[20];
    for (int g = 0; g < 20; g++) {
        uint32_t *grid = malloc(SIZE * SIZE * sizeof(uint32_t));
        for (int64_t r = 0; r < SIZE; r++)
            for (int64_t c = 0; c < SIZE; c++)
                grid[r * SIZE + c] = (r == 0 || c % 2 == 0) ? 'a' : (uint32_t)('a' + next_random(&seed) % 25 + 1);
        if (g % 2 == 1) {
            int64_t r = next_random(&seed) % (SIZE - 2) + 1;
            int64_t c = next_random(&seed) % (SIZE / 2 - 1) * 2 + 1;
            grid[r * SIZE + c] = 'a';
            grid[(r + 1) * SIZE + c] = 'a';
        }
        grids[g] = grid;
    }
    int64_t check = 0, found = 0;
    for (int64_t pass = 0; pass < 5; pass++) {
        for (int64_t g = 0; g < 20; g++) {
            int cycle = contains_cycle(grids[g], SIZE, SIZE);
            if (cycle) found++;
            check = mix(check, cycle ? pass * 20 + g : -1);
        }
    }
    printf("5 passes over 20 grids of 500 by 500: %lld with a cycle, checksum %lld\n", (long long)found,
           (long long)check);
    for (int g = 0; g < 20; g++) free(grids[g]);
    return 0;
}
