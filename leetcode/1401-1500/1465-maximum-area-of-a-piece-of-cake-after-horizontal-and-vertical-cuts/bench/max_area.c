// LeetCode #1465 bench in C: the ★ arm (each way's cuts sorted and its
// widest gap taken) on the same 100 cakes of 5000 cuts each way and 20
// passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}

static int64_t widest(int size, const int *cuts, int n, int *scratch) {
    memcpy(scratch, cuts, sizeof(int) * n);
    qsort(scratch, n, sizeof(int), cmp);
    int best = scratch[0];
    for (int i = 1; i < n; i++)
        if (scratch[i] - scratch[i - 1] > best) best = scratch[i] - scratch[i - 1];
    if (size - scratch[n - 1] > best) best = size - scratch[n - 1];
    return best;
}

static int64_t seed = 1465;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { CAKES = 100, CUTS = 5000 };
    int *across = malloc(sizeof(int) * CAKES * CUTS);
    int *down = malloc(sizeof(int) * CAKES * CUTS);
    int *scratch = malloc(sizeof(int) * CUTS);
    for (int c = 0; c < CAKES; c++) {
        for (int i = 0; i < CUTS; i++) {
            int64_t r = next_random() * 32768;
            across[c * CUTS + i] = (int)(1 + (r + next_random()) % 499999999);
        }
        for (int i = 0; i < CUTS; i++) {
            int64_t r = next_random() * 32768;
            down[c * CUTS + i] = (int)(1 + (r + next_random()) % 499999999);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 20; pass++) {
        for (int c = 0; c < CAKES; c++) {
            int h = (int)(1000000000 - check % 1000);
            int w = (int)(1000000000 - check / 1000 % 1000);
            int64_t a = widest(h, across + c * CUTS, CUTS, scratch);
            int64_t b = widest(w, down + c * CUTS, CUTS, scratch);
            int got = (int)(a * b % 1000000007);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("20 passes over 100 cakes of 5000 cuts each way: checksum %lld\n", (long long)check);
    free(across);
    free(down);
    free(scratch);
    return 0;
}
