// LeetCode #1284 bench, in C: the ★ arm (breadth-first search over bit
// masks) on every matrix of every shape, 1 by 1 to 3 by 3, 3000 rounds,
// every answer folded into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_flips(int64_t **mat, int64_t rows, int64_t cols) {
    int64_t cells = rows * cols, start = 0, flip[9], nflip = 0;
    for (int64_t i = 0; i < rows; i++)
        for (int64_t j = 0; j < cols; j++) {
            if (mat[i][j] == 1) start |= (int64_t)1 << (i * cols + j);
            int64_t mask = (int64_t)1 << (i * cols + j);
            if (i > 0) mask |= (int64_t)1 << ((i - 1) * cols + j);
            if (i + 1 < rows) mask |= (int64_t)1 << ((i + 1) * cols + j);
            if (j > 0) mask |= (int64_t)1 << (i * cols + j - 1);
            if (j + 1 < cols) mask |= (int64_t)1 << (i * cols + j + 1);
            flip[nflip++] = mask;
        }
    int64_t n = (int64_t)1 << cells;
    int64_t *dist = malloc(n * sizeof(int64_t));
    int64_t *queue = malloc(n * sizeof(int64_t));
    for (int64_t s = 0; s < n; s++) dist[s] = -1;
    int64_t head = 0, tail = 0, answer = -1;
    dist[start] = 0;
    queue[tail++] = start;
    while (head < tail) {
        int64_t state = queue[head++];
        if (state == 0) { answer = dist[state]; break; }
        for (int64_t k = 0; k < nflip; k++) {
            int64_t next = state ^ flip[k];
            if (dist[next] < 0) { dist[next] = dist[state] + 1; queue[tail++] = next; }
        }
    }
    free(dist);
    free(queue);
    return answer;
}

static int64_t **matrix(int64_t rows, int64_t cols, int64_t bits) {
    int64_t **mat = malloc(rows * sizeof(int64_t *));
    for (int64_t i = 0; i < rows; i++) {
        mat[i] = malloc(cols * sizeof(int64_t));
        for (int64_t j = 0; j < cols; j++) mat[i][j] = (bits >> (i * cols + j)) & 1;
    }
    return mat;
}

int main(void) {
    int64_t check = 0;
    for (int64_t round = 0; round < 3000; round++)
        for (int64_t rows = 1; rows < 4; rows++)
            for (int64_t cols = 1; cols < 4; cols++)
                for (int64_t bits = 0; bits < ((int64_t)1 << (rows * cols)); bits++) {
                    int64_t **mat = matrix(rows, cols, bits);
                    check = (check * 131 + min_flips(mat, rows, cols) + round + 2) % 1000000007;
                    for (int64_t i = 0; i < rows; i++) free(mat[i]);
                    free(mat);
                }
    printf("3000 rounds of every matrix: checksum %lld\n", (long long)check);
    return 0;
}
