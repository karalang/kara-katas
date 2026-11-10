// LeetCode #1109: Corporate Flight Bookings -- the bench in C: the ★ arm
// (a difference array and a running total) over 16 problems of 2 * 10^4
// flights and 2 * 10^4 bookings, each round changing one booking in every
// problem and solving it again. Each booking is its own heap array of
// three, as each is its own `Vec` in the other languages, and each call
// allocates its change array and its answer.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t *corp_flight_bookings(int64_t **bookings, int64_t m, int64_t n) {
    int64_t *change = calloc((size_t)(n + 1), sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        change[bookings[i][0] - 1] += bookings[i][2];
        change[bookings[i][1]] -= bookings[i][2];
    }
    int64_t *seats = malloc((size_t)n * sizeof(int64_t));
    int64_t running = 0;
    for (int64_t i = 0; i < n; i++) {
        running += change[i];
        seats[i] = running;
    }
    free(change);
    return seats;
}

static int64_t seed = 1109;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t *booking(int64_t n) {
    int64_t a = next_random() % n + 1;
    int64_t b = next_random() % n + 1;
    int64_t *v = malloc(3 * sizeof(int64_t));
    v[0] = a < b ? a : b;
    v[1] = a < b ? b : a;
    v[2] = next_random() % 10000 + 1;
    return v;
}

int main(void) {
    int64_t n = 20000;
    static int64_t *problems[16][20000];
    for (int j = 0; j < 16; j++)
        for (int i = 0; i < 20000; i++) problems[j][i] = booking(n);
    int64_t busiest = 0, check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int64_t j = 0; j < 16; j++) {
            int64_t at = (round * 7919 + j * 104729) % 20000;
            free(problems[j][at]);
            problems[j][at] = booking(n);
            int64_t *seats = corp_flight_bookings(problems[j], 20000, n);
            int64_t most = seats[0];
            for (int64_t i = 1; i < n; i++) if (seats[i] > most) most = seats[i];
            busiest += most;
            check = (check * 31 + seats[(round * 31 + j) % n]) % 1000000007;
            free(seats);
        }
    }
    printf("200 rounds over 16 problems of 20000 flights: busiest total %lld, checksum %lld\n", (long long)busiest, (long long)check);
    return 0;
}
