// LeetCode #2105: Watering Plants II -- bench, C mirror of
// watering.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimum_refill(const int64_t *plants, int64_t n, int64_t capacity_a, int64_t capacity_b) {
    int64_t i = 0, j = n - 1, a = capacity_a, b = capacity_b, refills = 0;
    while (i < j) {
        if (a < plants[i]) {
            refills++;
            a = capacity_a;
        }
        a -= plants[i];
        if (b < plants[j]) {
            refills++;
            b = capacity_b;
        }
        b -= plants[j];
        i++;
        j--;
    }
    if (i == j && (a > b ? a : b) < plants[i]) refills++;
    return refills;
}

static int64_t seed = 2105;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

#define ROWS 200
#define N 100000

int main(void) {
    int64_t *plants = malloc(sizeof(int64_t) * ROWS * N);
    int64_t caps[ROWS][2];
    for (int r = 0; r < ROWS; r++) {
        int64_t most = 0;
        for (int k = 0; k < N; k++) {
            int64_t x = wide_random() % 1000000 + 1;
            plants[(int64_t)r * N + k] = x;
            if (x > most) most = x;
        }
        int64_t a = most + wide_random() % (2000000 - most + 1);
        int64_t b = most + wide_random() % (2000000 - most + 1);
        caps[r][0] = a;
        caps[r][1] = b;
    }
    int64_t total = 0, check = 0;
    for (int p = 0; p < 10; p++)
        for (int r = 0; r < ROWS; r++) {
            int64_t got = minimum_refill(plants + (int64_t)r * N, N, caps[r][0], caps[r][1]);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    printf("2000 rows: %lld refills, checksum %lld\n", (long long)total, (long long)check);
    free(plants);
    return 0;
}
