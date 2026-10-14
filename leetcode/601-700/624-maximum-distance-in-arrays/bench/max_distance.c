// LeetCode #624: Maximum Distance in Arrays -- C mirror of the Kāra
// bench.
//
// The ★ arm's one pass over the same inputs and rounds; each input is an
// array of arrays, each with its length.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *values;
    int64_t len;
} Array;

static int64_t max_distance(const Array *arrays, int64_t count) {
    int64_t low = arrays[0].values[0];
    int64_t high = arrays[0].values[arrays[0].len - 1];
    int64_t best = 0;
    for (int64_t i = 1; i < count; i++) {
        int64_t first = arrays[i].values[0];
        int64_t last = arrays[i].values[arrays[i].len - 1];
        if (last - low > best) best = last - low;
        if (high - first > best) best = high - first;
        if (first < low) low = first;
        if (last > high) high = last;
    }
    return best;
}

static int64_t seed = 624;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int compare(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static Array *random_arrays(int64_t count, int64_t spread) {
    Array *arrays = malloc(count * sizeof(Array));
    for (int64_t i = 0; i < count; i++) {
        int64_t n = 1 + next_random() % 9;
        arrays[i].values = malloc(n * sizeof(int64_t));
        arrays[i].len = n;
        for (int64_t j = 0; j < n; j++) {
            arrays[i].values[j] = next_random() % (2 * spread + 1) - spread;
        }
        qsort(arrays[i].values, n, sizeof(int64_t), compare);
    }
    return arrays;
}

int main(void) {
    enum { INPUTS = 20, ROUNDS = 2000, COUNT = 20000 };
    Array *all[INPUTS];
    for (int i = 0; i < INPUTS; i++) {
        int64_t spread = 1000 + next_random() % 9001;
        all[i] = random_arrays(COUNT, spread);
    }
    int64_t sum = 0, checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t d = max_distance(all[(r * 7) % INPUTS], COUNT);
        sum += d;
        checksum = (checksum * 31 + d) % 1000000007;
    }
    printf("%d inputs, %d rounds: total %lld, checksum %lld\n", INPUTS, ROUNDS, (long long)sum, (long long)checksum);
    for (int i = 0; i < INPUTS; i++) {
        for (int64_t j = 0; j < COUNT; j++) {
            free(all[i][j].values);
        }
        free(all[i]);
    }
    return 0;
}
