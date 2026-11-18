// LeetCode #2274: Maximum Consecutive Floors Without Special Floors --
// the bench, the ★ arm. The floors are copied and sorted by `qsort`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_floor(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t max_consecutive(int64_t bottom, int64_t top, const int64_t *special, int64_t n) {
    int64_t *floors = malloc(n * sizeof(int64_t));
    memcpy(floors, special, n * sizeof(int64_t));
    qsort(floors, n, sizeof(int64_t), by_floor);
    int64_t best = floors[0] - bottom;
    if (top - floors[n - 1] > best) best = top - floors[n - 1];
    for (int64_t i = 1; i < n; i++) {
        int64_t run = floors[i] - floors[i - 1] - 1;
        if (run > best) best = run;
    }
    free(floors);
    return best;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2274;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    int64_t *special = malloc(100000 * sizeof(int64_t));
    for (int t = 0; t < 50; t++) {
        int64_t n = 0;
        int64_t f = 1 + next_random() % 20000;
        while (f <= 1000000000 && n < 100000) {
            special[n++] = f;
            f += 1 + next_random() % 20000;
        }
        for (int64_t j = n - 1; j >= 1; j--) {
            int64_t r = next_random() % (j + 1);
            int64_t tmp = special[j];
            special[j] = special[r];
            special[r] = tmp;
        }
        check = (check * 31 + max_consecutive(1, 1000000000, special, n)) % 1000000007;
    }
    free(special);
    printf("50 buildings of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
