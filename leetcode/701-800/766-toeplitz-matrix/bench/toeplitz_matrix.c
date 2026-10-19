// LeetCode 766 — Toeplitz Matrix: benchmark, the ★ arm in C.
// Sixteen 200 by 200 Toeplitz matrices, built once; 30,000 rounds of
// changing one cell, asking, and putting it back.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define SIZE 200

static int64_t seed = 766;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static bool is_toeplitz_matrix(int64_t **matrix, int m, int n) {
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            if (matrix[i][j] != matrix[i - 1][j - 1]) return false;
    return true;
}

int main(void) {
    int rounds = 30000;
    int64_t **pool[16];
    for (int k = 0; k < 16; k++) {
        int64_t diag[2 * SIZE - 1];
        for (int d = 0; d < 2 * SIZE - 1; d++) diag[d] = next_random() % 10;
        pool[k] = malloc(SIZE * sizeof(int64_t *));
        for (int i = 0; i < SIZE; i++) {
            pool[k][i] = malloc(SIZE * sizeof(int64_t));
            for (int j = 0; j < SIZE; j++) pool[k][i][j] = diag[i - j + SIZE - 1];
        }
    }
    int64_t yes = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int k = round % 16;
        int64_t i = next_random() % SIZE;
        int64_t j = next_random() % SIZE;
        int64_t old = pool[k][i][j];
        pool[k][i][j] = old + next_random() % 2;
        bool answer = is_toeplitz_matrix(pool[k], SIZE, SIZE);
        pool[k][i][j] = old;
        if (answer) yes++;
        check = (check * 31 + (answer ? 1 : 0) + i * SIZE + j) % 1000000007;
    }
    printf("%d rounds on 200 by 200: %lld Toeplitz, checksum %lld\n", rounds,
           (long long)yes, (long long)check);
    return 0;
}
