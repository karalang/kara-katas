// Benchmark for #490: C mirror of the ★ arm (breadth first over stopping
// cells); see the_maze.kara. The queue is a plain array: each cell joins
// it at most once.
#include <stdio.h>
#include <stdlib.h>

#define N 300
#define MAZES 60

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int has_path(const long long *maze, long long rows, long long cols,
                    const long long *start, const long long *destination) {
    static const long long STEP[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    char *seen = calloc(rows * cols, 1);
    long long *queue = malloc(sizeof(long long) * 2 * rows * cols);
    long long head = 0, tail = 0;
    queue[tail++] = start[0];
    queue[tail++] = start[1];
    seen[start[0] * cols + start[1]] = 1;
    int found = 0;
    while (head < tail) {
        long long row = queue[head++], col = queue[head++];
        if (row == destination[0] && col == destination[1]) {
            found = 1;
            break;
        }
        for (int d = 0; d < 4; d++) {
            long long dr = STEP[d][0], dc = STEP[d][1];
            long long r = row, c = col;
            while (r + dr >= 0 && r + dr < rows && c + dc >= 0 && c + dc < cols &&
                   maze[(r + dr) * cols + c + dc] == 0) {
                r += dr;
                c += dc;
            }
            if (!seen[r * cols + c]) {
                seen[r * cols + c] = 1;
                queue[tail++] = r;
                queue[tail++] = c;
            }
        }
    }
    free(seen);
    free(queue);
    return found;
}

int main(void) {
    // 60 mazes of 300 by 300 cells, a wall in each cell with odds of 1 in
    // 6, and a start and a destination on open cells, built once, then
    // each solved once.
    static long long mazes[MAZES][N * N], starts[MAZES][2], destinations[MAZES][2];
    long long seed = 490;
    for (int k = 0; k < MAZES; k++) {
        for (int i = 0; i < N * N; i++) {
            mazes[k][i] = next_random(&seed) % 6 == 0 ? 1 : 0;
        }
        starts[k][0] = next_random(&seed) % N;
        starts[k][1] = next_random(&seed) % N;
        destinations[k][0] = next_random(&seed) % N;
        destinations[k][1] = next_random(&seed) % N;
        mazes[k][starts[k][0] * N + starts[k][1]] = 0;
        mazes[k][destinations[k][0] * N + destinations[k][1]] = 0;
    }
    long long reached = 0, checksum = 0;
    for (int k = 0; k < MAZES; k++) {
        int found = has_path(mazes[k], N, N, starts[k], destinations[k]);
        if (found) {
            reached++;
        }
        checksum = (checksum * 31 + (found ? 7 : 3)) % 1000000007;
    }
    printf("60 mazes of 300 by 300: the destination reached in %lld, checksum %lld\n", reached, checksum);
    return 0;
}
