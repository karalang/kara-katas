// Benchmark for #605: C mirror of the ★ arm (plant greedily); see
// can_place_flowers.kara. The bed is copied into a `malloc`'d buffer on
// every call, as the Kāra arm clones it, and freed after.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool can_place_flowers(const int64_t *flowerbed, int64_t len, int64_t n) {
    int64_t *bed = malloc((size_t)len * sizeof *bed);
    memcpy(bed, flowerbed, (size_t)len * sizeof *bed);
    int64_t planted = 0;
    for (int64_t i = 0; i < len; i++) {
        if (bed[i] == 0 && (i == 0 || bed[i - 1] == 0) && (i == len - 1 || bed[i + 1] == 0)) {
            bed[i] = 1;
            planted++;
        }
    }
    free(bed);
    return planted >= n;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 100, ROUNDS = 50, SIZE = 20000 };
    int64_t seed = 605;
    static int64_t beds[COUNT][SIZE];
    for (int b = 0; b < COUNT; b++) {
        int64_t spread = 2 + step(&seed) % 5;
        for (int i = 0; i < SIZE; i++)
            beds[b][i] = step(&seed) % spread == 0 && (i == 0 || beds[b][i - 1] == 0) ? 1 : 0;
    }
    int64_t yes = 0, checksum = 0;
    for (int64_t round = 0; round < ROUNDS; round++)
        for (int64_t g = 0; g < COUNT; g++) {
            int64_t n = (round * 397 + g * 113) % 8000;
            bool fits = can_place_flowers(beds[(round * 7 + g) % COUNT], SIZE, n);
            if (fits) yes++;
            checksum = (checksum * 31 + n * 2 + (fits ? 1 : 0)) % 1000000007;
        }
    printf("%d beds, %d rounds: %lld fit, checksum %lld\n", COUNT, ROUNDS, (long long)yes, (long long)checksum);
    return 0;
}
