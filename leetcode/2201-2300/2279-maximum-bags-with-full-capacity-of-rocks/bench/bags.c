// LeetCode #2279: Maximum Bags With Full Capacity of Rocks -- the bench,
// the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t maximum_bags(const int64_t *capacity, const int64_t *rocks, int64_t n,
                            int64_t additional_rocks) {
    int64_t *lack = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) lack[i] = capacity[i] - rocks[i];
    qsort(lack, n, sizeof(int64_t), cmp);
    int64_t left = additional_rocks, full = 0;
    for (int64_t i = 0; i < n; i++) {
        if (lack[i] > left) break;
        left -= lack[i];
        full++;
    }
    free(lack);
    return full;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2279;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t draw(int64_t high) {
    int64_t top = next_random();
    return (top * 32768 + next_random()) % high;
}

int main(void) {
    int64_t check = 0;
    int64_t *capacity = malloc(50000 * sizeof(int64_t));
    int64_t *rocks = malloc(50000 * sizeof(int64_t));
    for (int t = 0; t < 50; t++) {
        for (int i = 0; i < 50000; i++) {
            int64_t c = draw(1000000000) + 1;
            capacity[i] = c;
            rocks[i] = draw(c + 1);
        }
        int64_t spare = draw(1000000000) + 1;
        check = (check * 31 + maximum_bags(capacity, rocks, 50000, spare)) % 1000000007;
    }
    free(capacity);
    free(rocks);
    printf("50 sets of 5 * 10^4: checksum %lld\n", (long long)check);
    return 0;
}
