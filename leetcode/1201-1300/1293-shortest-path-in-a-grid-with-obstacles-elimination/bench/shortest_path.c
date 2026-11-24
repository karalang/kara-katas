// LeetCode #1293 bench: the ★ arm over 50 grids of 40 by 40 with obstacles 30
// in 100, built once; then 80 passes, each flipping one cell of every grid and
// choosing k from the checksum so far, answering it. The queue is a ring
// buffer grown by doubling, and `best` a fresh allocation per call, as the
// other languages' are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { M = 40, N = 40, GRIDS = 50 };

typedef struct {
    int64_t r, c, left;
} State;

typedef struct {
    State *buf;
    size_t cap, head, len;
} Queue;

static void push(Queue *q, State s) {
    if (q->len == q->cap) {
        size_t cap = q->cap ? q->cap * 2 : 8;
        State *buf = malloc(sizeof(State) * cap);
        for (size_t i = 0; i < q->len; i++) {
            buf[i] = q->buf[(q->head + i) % q->cap];
        }
        free(q->buf);
        q->buf = buf;
        q->cap = cap;
        q->head = 0;
    }
    q->buf[(q->head + q->len) % q->cap] = s;
    q->len++;
}

static State pop(Queue *q) {
    State s = q->buf[q->head];
    q->head = (q->head + 1) % q->cap;
    q->len--;
    return s;
}

static int64_t shortest_path(int64_t grid[M][N], int64_t m, int64_t n, int64_t k) {
    if (k >= m + n - 2) {
        return m + n - 2;
    }
    int64_t *best = malloc(sizeof(int64_t) * m * n);
    for (int64_t i = 0; i < m * n; i++) {
        best[i] = -1;
    }
    Queue q = {0};
    push(&q, (State){0, 0, k});
    best[0] = k;
    int64_t steps = 0;
    static const int dr[4] = {1, -1, 0, 0};
    static const int dc[4] = {0, 0, 1, -1};
    int64_t answer = -1;
    while (q.len > 0) {
        size_t level = q.len;
        for (size_t t = 0; t < level; t++) {
            State s = pop(&q);
            if (s.r == m - 1 && s.c == n - 1) {
                answer = steps;
                goto done;
            }
            for (int d = 0; d < 4; d++) {
                int64_t nr = s.r + dr[d];
                int64_t nc = s.c + dc[d];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) {
                    continue;
                }
                int64_t rest = s.left - grid[nr][nc];
                if (rest > best[nr * n + nc]) {
                    best[nr * n + nc] = rest;
                    push(&q, (State){nr, nc, rest});
                }
            }
        }
        steps++;
    }
done:
    free(q.buf);
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t grids[GRIDS][M][N];

int main(void) {
    int64_t seed = 1293;
    for (int a = 0; a < GRIDS; a++) {
        for (int i = 0; i < M; i++) {
            for (int j = 0; j < N; j++) {
                int corner = (i == 0 && j == 0) || (i == 39 && j == 39);
                grids[a][i][j] = (!corner && next_random(&seed) % 100 < 30) ? 1 : 0;
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 80; p++) {
        for (int a = 0; a < GRIDS; a++) {
            int64_t cell = 1 + check % 1598;
            grids[a][cell / 40][cell % 40] = 1 - grids[a][cell / 40][cell % 40];
            check = (check * 31 + shortest_path(grids[a], M, N, check % 78) + 2 + p) % 1000000007;
        }
    }
    printf("80 passes over 50 grids of 40 by 40: checksum %lld\n", (long long)check);
    return 0;
}
