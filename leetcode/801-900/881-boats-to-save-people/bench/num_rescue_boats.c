// LeetCode #881 bench: C mirror of num_rescue_boats.kara (the ★ arm, sort,
// then two pointers) on the same 600 cases. The sort is the C library's
// qsort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_weight(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t num_rescue_boats(const int64_t *people, int64_t n, int64_t limit) {
    int64_t *weights = malloc((size_t)n * sizeof *weights);
    memcpy(weights, people, (size_t)n * sizeof *weights);
    qsort(weights, (size_t)n, sizeof *weights, by_weight);
    int64_t light = 0, heavy = n - 1, boats = 0;
    while (light <= heavy) {
        if (weights[light] + weights[heavy] <= limit) {
            light++;
        }
        heavy--;
        boats++;
    }
    free(weights);
    return boats;
}

static int64_t seed = 881;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    int64_t *people = malloc(50000 * sizeof *people);
    for (int k = 0; k < 600; k++) {
        int64_t n = 40000 + next_random() % 10001;
        int64_t x = next_random();
        int64_t y = next_random();
        int64_t limit = 1 + (x * 32768 + y) % 30000;
        for (int64_t i = 0; i < n; i++) {
            int64_t a = next_random();
            int64_t b = next_random();
            people[i] = (a * 32768 + b) % limit + 1;
        }
        int64_t boats = num_rescue_boats(people, n, limit);
        total += boats;
        check = (check * 131 + boats) % 1000000007;
    }
    free(people);
    printf("600 cases of up to 50000 people: %lld boats, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
