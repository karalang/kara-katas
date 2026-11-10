// LeetCode #1105: Filling Bookcase Shelves -- the bench in C: the ★ arm
// (the least height for the first i books over every run ending at book
// i that fits a shelf) over 32 bookcases of 1000 books, each round
// changing one book in every bookcase and solving it again.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t min_height_shelves(int64_t (*books)[2], int64_t n, int64_t shelf_width) {
    int64_t *best = calloc((size_t)(n + 1), sizeof(int64_t));
    for (int64_t i = 1; i <= n; i++) {
        int64_t width = 0, tallest = 0;
        best[i] = INT64_MAX;
        int64_t j = i;
        while (j > 0 && width + books[j - 1][0] <= shelf_width) {
            width += books[j - 1][0];
            if (books[j - 1][1] > tallest) tallest = books[j - 1][1];
            if (best[j - 1] + tallest < best[i]) best[i] = best[j - 1] + tallest;
            j -= 1;
        }
    }
    int64_t h = best[n];
    free(best);
    return h;
}

static int64_t seed = 1105;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t cases[32][1000][2];
    for (int c = 0; c < 32; c++)
        for (int i = 0; i < 1000; i++) {
            int64_t t = next_random() % 50 + 1;
            cases[c][i][0] = t;
            cases[c][i][1] = next_random() % 1000 + 1;
        }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int64_t j = 0; j < 32; j++) {
            int64_t at = (round * 7919 + j * 104729) % 1000;
            cases[j][at][0] = (cases[j][at][0] * 7 + round) % 50 + 1;
            cases[j][at][1] = (cases[j][at][1] * 13 + j) % 1000 + 1;
            int64_t h = min_height_shelves(cases[j], 1000, 1000);
            total += h;
            check = (check * 31 + h) % 1000000007;
        }
    }
    printf("200 rounds over 32 bookcases of 1000 books: heights total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
