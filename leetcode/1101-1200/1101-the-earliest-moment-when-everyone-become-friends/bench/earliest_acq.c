// Benchmark: LeetCode #1101 The Earliest Moment When Everyone Become
// Friends -- union-find over the logs in time order, as the Kāra ★ arm.
// Each call copies the logs, each log its own heap array as in the Kāra
// and Rust benches, and sorts the copy with qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define M 4950

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int by_time(const void *a, const void *b) {
    int64_t x = (*(int64_t *const *)a)[0], y = (*(int64_t *const *)b)[0];
    return (x > y) - (x < y);
}

static int64_t earliest_acq(int64_t **logs, int m, int64_t n) {
    int64_t **copy = malloc(m * sizeof *copy);
    for (int i = 0; i < m; i++) {
        copy[i] = malloc(3 * sizeof(int64_t));
        memcpy(copy[i], logs[i], 3 * sizeof(int64_t));
    }
    qsort(copy, m, sizeof *copy, by_time);
    int64_t *parent = malloc(n * sizeof *parent), *size = malloc(n * sizeof *size);
    for (int64_t i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    int64_t groups = n, answer = -1;
    for (int i = 0; i < m; i++) {
        int64_t a = find(parent, copy[i][1]), b = find(parent, copy[i][2]);
        if (a == b) continue;
        int64_t big = size[a] >= size[b] ? a : b, small = big == a ? b : a;
        parent[small] = big;
        size[big] += size[small];
        if (--groups == 1) { answer = copy[i][0]; break; }
    }
    for (int i = 0; i < m; i++) free(copy[i]);
    free(copy); free(parent); free(size);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1101;
    static int64_t *groups[64][M];
    for (int g = 0; g < 64; g++) {
        int64_t times[M];
        for (int i = 0; i < M; i++) times[i] = i;
        for (int i = M - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) % (i + 1), t = times[i];
            times[i] = times[j]; times[j] = t;
        }
        int k = 0;
        for (int64_t x = 0; x < 100; x++)
            for (int64_t y = x + 1; y < 100; y++) {
                int64_t *log = malloc(3 * sizeof(int64_t));
                log[0] = times[k] * 1000; log[1] = x; log[2] = y;
                groups[g][k++] = log;
            }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 20; round++)
        for (int64_t j = 0; j < 64; j++) {
            int64_t a = (round * 7919 + j * 104729) % M, b = (round * 31 + j * 17 + 1) % M;
            int64_t t = groups[j][a][0];
            groups[j][a][0] = groups[j][b][0];
            groups[j][b][0] = t;
            int64_t moment = earliest_acq(groups[j], M, 100);
            total += moment;
            check = (check * 31 + moment + 2) % 1000000007;
        }
    printf("20 rounds over 64 groups of 100 people: moments sum to %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
