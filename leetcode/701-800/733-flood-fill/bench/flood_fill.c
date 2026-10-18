// LeetCode #733: Flood Fill -- depth first, with a stack of places.
// Benchmark mirror of the Kara star arm: push the start; pop a place,
// and if it still has the old color, paint it and push its four
// neighbours.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t r, c;
} Place;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void flood_fill(int64_t **img, int64_t m, int64_t n, int64_t sr, int64_t sc, int64_t color) {
    int64_t old = img[sr][sc];
    if (old == color) return;
    int64_t len = 0, cap = 4;
    Place *stack = malloc(cap * sizeof(Place));
    stack[len++] = (Place){sr, sc};
    while (len > 0) {
        Place p = stack[--len];
        int64_t r = p.r, c = p.c;
        if (r < 0 || r >= m || c < 0 || c >= n || img[r][c] != old) continue;
        img[r][c] = color;
        if (len + 4 > cap) {
            cap *= 2;
            stack = realloc(stack, cap * sizeof(Place));
        }
        stack[len++] = (Place){r + 1, c};
        stack[len++] = (Place){r - 1, c};
        stack[len++] = (Place){r, c + 1};
        stack[len++] = (Place){r, c - 1};
    }
    free(stack);
}

int main(void) {
    int64_t seed = 733, size = 1000;
    int64_t **img = malloc(size * sizeof(int64_t *));
    for (int64_t r = 0; r < size; r++) {
        img[r] = malloc(size * sizeof(int64_t));
        for (int64_t c = 0; c < size; c++) img[r][c] = next_random(&seed) % 3 == 0 ? 1 : 0;
    }
    int64_t sum = 0;
    for (int64_t round = 0; round < 40; round++) {
        int64_t r = (next_random(&seed) * 32768 + next_random(&seed)) % size;
        int64_t c = (next_random(&seed) * 32768 + next_random(&seed)) % size;
        int64_t old = img[r][c];
        flood_fill(img, size, size, r, c, 2);
        for (int64_t x = 0; x < size; x++)
            if (img[r][x] == 2) sum++;
        flood_fill(img, size, size, r, c, old);
    }
    int64_t zeros = 0;
    for (int64_t r = 0; r < size; r++)
        for (int64_t c = 0; c < size; c++)
            if (img[r][c] == 0) zeros++;
    printf("40 rounds on a 1000 x 1000 image: %lld painted in their rows, %lld 0s after\n", (long long)sum,
           (long long)zeros);
    for (int64_t r = 0; r < size; r++) free(img[r]);
    free(img);
    return 0;
}
