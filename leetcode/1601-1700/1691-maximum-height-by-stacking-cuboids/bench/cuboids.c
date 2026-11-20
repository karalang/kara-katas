// LeetCode #1691: Maximum Height by Stacking Cuboids -- the bench's C
// mirror: the ★ arm on 3000 random sets of 100 cuboids, all drawn first,
// each answered 5 times. The sorted copy and the table are malloc'd per
// answer, as the other languages build them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 3000
#define SIZE 100
#define ROUNDS 5

static int by_sides(const void *x, const void *y) {
    const int32_t *a = x, *b = y;
    for (int d = 0; d < 3; d++) {
        if (a[d] != b[d]) return (a[d] > b[d]) - (a[d] < b[d]);
    }
    return 0;
}

static int32_t max_height(const int32_t (*cuboids)[3], int64_t n) {
    int32_t (*boxes)[3] = malloc((size_t)n * sizeof *boxes);
    memcpy(boxes, cuboids, (size_t)n * sizeof *boxes);
    for (int64_t i = 0; i < n; i++) {
        // three sides sorted by insertion
        for (int a = 1; a < 3; a++)
            for (int b = a; b > 0 && boxes[i][b - 1] > boxes[i][b]; b--) {
                int32_t t = boxes[i][b];
                boxes[i][b] = boxes[i][b - 1];
                boxes[i][b - 1] = t;
            }
    }
    qsort(boxes, (size_t)n, sizeof *boxes, by_sides);
    int32_t *best = malloc((size_t)n * sizeof *best);
    int32_t tallest = 0;
    for (int64_t i = 0; i < n; i++) {
        best[i] = boxes[i][2];
        for (int64_t j = 0; j < i; j++) {
            if (boxes[j][0] <= boxes[i][0] && boxes[j][1] <= boxes[i][1] && boxes[j][2] <= boxes[i][2]) {
                int32_t v = best[j] + boxes[i][2];
                if (v > best[i]) best[i] = v;
            }
        }
        if (best[i] > tallest) tallest = best[i];
    }
    free(boxes);
    free(best);
    return tallest;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1691;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t sets[COUNT][SIZE][3];
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < SIZE; i++)
            for (int d = 0; d < 3; d++) sets[c][i][d] = (int32_t)(next_random() % 100 + 1);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int32_t answer = max_height((const int32_t(*)[3])sets[c], SIZE);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d sets of %d cuboids, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, SIZE, ROUNDS, (long long)total, (long long)check);
    return 0;
}
