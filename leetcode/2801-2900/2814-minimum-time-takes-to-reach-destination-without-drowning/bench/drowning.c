// LeetCode #2814: Minimum Time Takes to Reach Destination Without
// Drowning -- the bench in C: the ★ arm over 200 lands of 100 by 100, a
// cell in five stone and one in 5000 flooded, all drawn first, then each
// answered 5 times. Each cell is one `char` rather than a string, and the
// queue an array of n * n cells.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100
#define COUNT 200
#define NEVER INT64_MAX

static const int DR[4] = {0, 1, 0, -1};
static const int DC[4] = {1, 0, -1, 0};

static int64_t seed = 2814;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char lands[COUNT][N][N];
static int64_t flood[N][N], when[N][N];
static int64_t queue_r[N * N], queue_c[N * N];

static int64_t minimum_seconds(char (*land)[N], int64_t n, int64_t m) {
    int64_t head = 0, tail = 0;
    for (int64_t r = 0; r < n; r++)
        for (int64_t c = 0; c < m; c++) {
            flood[r][c] = NEVER;
            when[r][c] = -1;
            if (land[r][c] == '*') {
                flood[r][c] = 0;
                queue_r[tail] = r;
                queue_c[tail++] = c;
            }
        }
    while (head < tail) {
        int64_t r = queue_r[head], c = queue_c[head++];
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + DR[d], nc = c + DC[d];
            if (nr >= 0 && nr < n && nc >= 0 && nc < m && flood[nr][nc] == NEVER &&
                (land[nr][nc] == '.' || land[nr][nc] == 'S')) {
                flood[nr][nc] = flood[r][c] + 1;
                queue_r[tail] = nr;
                queue_c[tail++] = nc;
            }
        }
    }
    head = tail = 0;
    for (int64_t r = 0; r < n; r++)
        for (int64_t c = 0; c < m; c++)
            if (land[r][c] == 'S') {
                when[r][c] = 0;
                queue_r[tail] = r;
                queue_c[tail++] = c;
            }
    while (head < tail) {
        int64_t r = queue_r[head], c = queue_c[head++];
        if (land[r][c] == 'D') return when[r][c];
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + DR[d], nc = c + DC[d];
            if (nr >= 0 && nr < n && nc >= 0 && nc < m && when[nr][nc] == -1 && land[nr][nc] != 'X' &&
                flood[nr][nc] > when[r][c] + 1) {
                when[nr][nc] = when[r][c] + 1;
                queue_r[tail] = nr;
                queue_c[tail++] = nc;
            }
        }
    }
    return -1;
}

int main(void) {
    int rounds = 5;
    for (int g = 0; g < COUNT; g++) {
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) {
                int64_t roll = next_random() % 10000;
                lands[g][r][c] = roll < 2000 ? 'X' : roll < 2002 ? '*' : '.';
            }
        int64_t start = next_random() % (N * N);
        int64_t end = next_random() % (N * N - 1);
        if (end >= start) end++;
        lands[g][start / N][start % N] = 'S';
        lands[g][end / N][end % N] = 'D';
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int g = 0; g < COUNT; g++) {
            int64_t a = minimum_seconds(lands[g], N, N);
            total += a;
            check = (check * 31 + a + 2 + r) % 1000000007;
        }
    printf("%d lands of %d by %d, %d rounds: seconds sum to %lld, checksum %lld\n", COUNT, N, N, rounds, (long long)total, (long long)check);
    return 0;
}
