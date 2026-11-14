// LeetCode #2126: Destroying Asteroids -- the benchmark, the same
// algorithm as asteroids.kara; the copy sorted with qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static int64_t seed = 2126;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int asteroids_destroyed(int64_t mass, const int64_t *asteroids, int64_t *sorted) {
    memcpy(sorted, asteroids, sizeof(int64_t) * N);
    qsort(sorted, N, sizeof(int64_t), cmp);
    int64_t planet = mass;
    for (int i = 0; i < N; i++) {
        if (planet < sorted[i]) return 0;
        planet += sorted[i];
    }
    return 1;
}

int main(void) {
    int64_t *arrays = malloc(sizeof(int64_t) * 20 * N);
    int64_t *sorted = malloc(sizeof(int64_t) * N);
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            arrays[k * N + i] = (hi * 32768 + next_random()) % 99001 + 1000;
        }
    int64_t destroyed = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int64_t k = 0; k < 20; k++) {
            int64_t hi = next_random();
            int64_t at = (hi * 32768 + next_random()) % 100000;
            arrays[k * N + at] = next_random() % 2000 + 1;
            int64_t mass = next_random() % 1000 + 500;
            if (asteroids_destroyed(mass, arrays + k * N, sorted)) {
                destroyed++;
                check = (check * 31 + round * 20 + k) % 1000000007;
            }
        }
    }
    printf("200 solves: %lld destroyed, checksum %lld\n", (long long)destroyed, (long long)check);
    free(arrays);
    free(sorted);
    return 0;
}
