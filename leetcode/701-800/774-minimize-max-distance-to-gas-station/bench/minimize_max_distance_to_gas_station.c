// LeetCode 774 — Minimize Max Distance to Gas Station: benchmark, the ★
// arm in C. Sixty-four random roads of 2,000 stations, LeetCode's limit,
// spread over up to 10^8, each with k from 1 to 10^6, built once; ROUNDS
// rounds each solve the next of them.
#include <stdio.h>
#include <stdint.h>

#define ROUNDS 2000
#define N 2000

static double minmax_gas_dist(const int64_t *stations, int n, int64_t k) {
    double lo = 0.0, hi = 0.0;
    for (int i = 1; i < n; i++) {
        double gap = (double)(stations[i] - stations[i - 1]);
        if (gap > hi) hi = gap;
    }
    hi += 1.0;
    for (int it = 0; it < 100; it++) {
        double mid = (lo + hi) / 2.0;
        int64_t needed = 0;
        for (int i = 1; i < n; i++) needed += (int64_t)((double)(stations[i] - stations[i - 1]) / mid);
        if (needed <= k)
            hi = mid;
        else
            lo = mid;
    }
    double longest = 0.0;
    for (int i = 1; i < n; i++) {
        double gap = (double)(stations[i] - stations[i - 1]);
        double piece = gap / (double)((int64_t)(gap / hi) + 1);
        if (piece > longest) longest = piece;
    }
    return longest;
}

static int64_t seed = 774;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t roads[64][N];
static int64_t ks[64];

int main(void) {
    for (int r = 0; r < 64; r++) {
        roads[r][0] = next_random() % 100;
        for (int i = 1; i < N; i++) {
            int64_t a = next_random();
            int64_t b = next_random();
            roads[r][i] = roads[r][i - 1] + 1 + (a * 32768 + b) % 50000;
        }
        int64_t a = next_random();
        int64_t b = next_random();
        ks[r] = 1 + (a * 32768 + b) % 1000000;
    }
    double total = 0.0;
    for (int64_t round = 0; round < ROUNDS; round++) total += minmax_gas_dist(roads[round % 64], N, ks[round % 64]);
    printf("%d roads of 2000 stations: answers sum to %.5f\n", ROUNDS, total);
    return 0;
}
