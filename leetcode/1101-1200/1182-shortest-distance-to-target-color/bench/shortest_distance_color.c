// LeetCode #1182: Shortest Distance to Target Color -- the ★ arm in C: a
// nearest-distance table per colour, filled from each side, then a lookup a
// query. Each call allocates its tables and its answer, and frees them, as
// the Kāra and Rust versions do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *shortest_distance_color(const int64_t *colors, int64_t n, int64_t **queries, int64_t q) {
    int64_t far = n + 1;
    int64_t *nearest[3];
    for (int64_t c = 1; c <= 3; c++) {
        int64_t *dist = malloc(sizeof(int64_t) * n);
        for (int64_t i = 0; i < n; i++) dist[i] = far;
        int64_t last = -1;
        for (int64_t i = 0; i < n; i++) {
            if (colors[i] == c) last = i;
            if (last >= 0) dist[i] = i - last;
        }
        last = -1;
        for (int64_t i = n - 1; i >= 0; i--) {
            if (colors[i] == c) last = i;
            if (last >= 0 && last - i < dist[i]) dist[i] = last - i;
        }
        nearest[c - 1] = dist;
    }
    int64_t *answer = malloc(sizeof(int64_t) * q);
    for (int64_t k = 0; k < q; k++) {
        int64_t d = nearest[queries[k][1] - 1][queries[k][0]];
        answer[k] = d == far ? -1 : d;
    }
    for (int c = 0; c < 3; c++) free(nearest[c]);
    return answer;
}

static int64_t seed = 1182;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { N = 50000, Q = 50000, A = 4 };
    int64_t *arrays[A];
    int64_t **asks[A];
    for (int a = 0; a < A; a++) {
        arrays[a] = malloc(sizeof(int64_t) * N);
        for (int i = 0; i < N; i++) arrays[a][i] = next_random() % 997 == 0 ? 3 : 1 + next_random() % 2;
        asks[a] = malloc(sizeof(int64_t *) * Q);
        for (int k = 0; k < Q; k++) {
            asks[a][k] = malloc(sizeof(int64_t) * 2);
            asks[a][k][0] = next_random() % N;
            asks[a][k][1] = 1 + next_random() % 3;
        }
    }
    int64_t rounds = 40, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int a = 0; a < A; a++) {
            int64_t *got = shortest_distance_color(arrays[a], N, asks[a], Q);
            for (int k = 0; k < Q; k++) check = (check * 131 + got[k] + 2 + round) % 1000000007;
            free(got);
        }
    }
    printf("%lld rounds of 4 arrays of 50000 queries: checksum %lld\n", (long long)rounds, (long long)check);
    return 0;
}
