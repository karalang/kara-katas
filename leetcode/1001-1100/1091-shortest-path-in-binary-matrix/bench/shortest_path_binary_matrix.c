// Benchmark: LeetCode #1091 Shortest Path in Binary Matrix -- C mirror of the
// ★ arm: breadth-first search with a ring-buffer queue and a grid of
// distances, both allocated per call as the Kāra arm's are. Same workload
// and sink as shortest_path_binary_matrix.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define GRIDS 200
#define N 100

static int64_t shortest_path_binary_matrix(int64_t **grid, int64_t n) {
    if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) {
        return -1;
    }
    int64_t *dist = malloc(n * n * sizeof(int64_t));
    for (int64_t i = 0; i < n * n; i++) {
        dist[i] = -1;
    }
    // every cell is queued at most once, so n * n slots never wrap
    int64_t *qr = malloc(n * n * sizeof(int64_t)), *qc = malloc(n * n * sizeof(int64_t));
    int64_t head = 0, tail = 0, answer = -1;
    dist[0] = 1;
    qr[tail] = 0;
    qc[tail++] = 0;
    while (head < tail) {
        int64_t r = qr[head], c = qc[head++];
        if (r == n - 1 && c == n - 1) {
            answer = dist[r * n + c];
            break;
        }
        for (int64_t dr = -1; dr <= 1; dr++) {
            for (int64_t dc = -1; dc <= 1; dc++) {
                int64_t nr = r + dr, nc = c + dc;
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 0 && dist[nr * n + nc] == -1) {
                    dist[nr * n + nc] = dist[r * n + c] + 1;
                    qr[tail] = nr;
                    qc[tail++] = nc;
                }
            }
        }
    }
    free(dist);
    free(qr);
    free(qc);
    return answer;
}

static int64_t seed = 1091;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t **grids[GRIDS];
    for (int k = 0; k < GRIDS; k++) {
        int64_t blocked = 25 + k % 20;
        grids[k] = malloc(N * sizeof(int64_t *));
        for (int r = 0; r < N; r++) {
            grids[k][r] = malloc(N * sizeof(int64_t));
            for (int c = 0; c < N; c++) {
                grids[k][r][c] = next_random() % 100 < blocked ? 1 : 0;
            }
        }
        grids[k][0][0] = 0;
        grids[k][N - 1][N - 1] = 0;
    }
    int64_t none = 0, total = 0, check = 0;
    for (int round = 0; round < 20; round++) {
        for (int k = 0; k < GRIDS; k++) {
            int64_t answer = shortest_path_binary_matrix(grids[k], N);
            if (answer == -1) {
                none++;
            } else {
                total += answer;
            }
            check = (check * 31 + answer + 1) % 1000000007;
        }
    }
    printf("20 rounds over 200 grids of 100 by 100: %lld without a path, lengths sum to %lld, checksum %lld\n",
           (long long)none, (long long)total, (long long)check);
    for (int k = 0; k < GRIDS; k++) {
        for (int r = 0; r < N; r++) {
            free(grids[k][r]);
        }
        free(grids[k]);
    }
    return 0;
}
