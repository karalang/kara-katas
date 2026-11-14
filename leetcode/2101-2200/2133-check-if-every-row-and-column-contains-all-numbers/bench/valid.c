// LeetCode #2133: Check if Every Row and Column Contains All Numbers --
// the benchmark, the same algorithm as valid.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

static int check_valid(int64_t **matrix, int64_t n) {
    int64_t *mark = malloc((size_t)(n + 1) * sizeof(int64_t));
    for (int64_t v = 0; v <= n; v++) mark[v] = -1;
    int ok = 1;
    for (int64_t i = 0; i < n && ok; i++) {
        for (int64_t j = 0; j < n; j++) {
            int64_t v = matrix[i][j];
            if (mark[v] == 2 * i) { ok = 0; break; }
            mark[v] = 2 * i;
        }
        if (!ok) break;
        for (int64_t j = 0; j < n; j++) {
            int64_t v = matrix[j][i];
            if (mark[v] == 2 * i + 1) { ok = 0; break; }
            mark[v] = 2 * i + 1;
        }
    }
    free(mark);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t **latin(int64_t n, int64_t *seed) {
    int64_t rows[N], symbols[N];
    for (int64_t i = 0; i < n; i++) { rows[i] = i; symbols[i] = i + 1; }
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = next_random(seed) % (i + 1), t = rows[i];
        rows[i] = rows[j]; rows[j] = t;
        j = next_random(seed) % (i + 1); t = symbols[i];
        symbols[i] = symbols[j]; symbols[j] = t;
    }
    int64_t **m = malloc((size_t)n * sizeof(int64_t *));
    for (int64_t r = 0; r < n; r++) {
        m[r] = malloc((size_t)n * sizeof(int64_t));
        for (int64_t c = 0; c < n; c++) m[r][c] = symbols[(rows[r] + c) % n];
    }
    return m;
}

int main(void) {
    int64_t seed = 2133;
    int64_t **squares[10];
    for (int k = 0; k < 10; k++) squares[k] = latin(N, &seed);
    int64_t valid = 0, check = 0;
    for (int64_t round = 0; round < 20000; round++) {
        int64_t k = next_random(&seed) % 10;
        int64_t r = next_random(&seed) % 100;
        int64_t a = next_random(&seed) % 100;
        int64_t b = next_random(&seed) % 100;
        int ok;
        if (round % 2 == 1) {
            int64_t *t = squares[k][a]; squares[k][a] = squares[k][b]; squares[k][b] = t;
            ok = check_valid(squares[k], N);
        } else {
            int64_t t = squares[k][r][a]; squares[k][r][a] = squares[k][r][b]; squares[k][r][b] = t;
            ok = check_valid(squares[k], N);
            t = squares[k][r][a]; squares[k][r][a] = squares[k][r][b]; squares[k][r][b] = t;
        }
        valid += ok;
        check = (check * 31 + ok + squares[k][r][a]) % 1000000007;
    }
    printf("20000 solves: %lld valid, checksum %lld\n", (long long)valid, (long long)check);
    for (int k = 0; k < 10; k++) {
        for (int r = 0; r < N; r++) free(squares[k][r]);
        free(squares[k]);
    }
    return 0;
}
