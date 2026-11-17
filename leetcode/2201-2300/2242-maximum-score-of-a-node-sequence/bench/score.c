// LeetCode #2242: Maximum Score of a Node Sequence -- the benchmark's C
// mirror of score.kara: each node's neighbours sorted by score, largest
// first, and cut to three; every edge as the middle one tries the nine
// pairs, all four distinct. The neighbours are kept in one array indexed
// by offsets (CSR) rather than a list per node.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 50000

static const int64_t *score_of;

static int by_score_desc(const void *x, const void *y) {
    int64_t a = score_of[*(const int64_t *)x], b = score_of[*(const int64_t *)y];
    return a < b ? 1 : a > b ? -1 : 0;
}

static int64_t maximum_score(const int64_t *scores, const int64_t (*edges)[2], int64_t n, int64_t m) {
    int64_t *degree = calloc(n + 1, sizeof(int64_t));
    int64_t *start = malloc((n + 1) * sizeof(int64_t));
    int64_t *near = malloc(2 * m * sizeof(int64_t));
    int64_t *kept = malloc(n * sizeof(int64_t));
    for (int64_t j = 0; j < m; j++) {
        degree[edges[j][0]]++;
        degree[edges[j][1]]++;
    }
    start[0] = 0;
    for (int64_t i = 0; i < n; i++) start[i + 1] = start[i] + degree[i];
    for (int64_t i = 0; i < n; i++) degree[i] = 0;
    for (int64_t j = 0; j < m; j++) {
        int64_t a = edges[j][0], b = edges[j][1];
        near[start[a] + degree[a]++] = b;
        near[start[b] + degree[b]++] = a;
    }
    score_of = scores;
    for (int64_t i = 0; i < n; i++) {
        qsort(near + start[i], degree[i], sizeof(int64_t), by_score_desc);
        kept[i] = degree[i] < 3 ? degree[i] : 3;
    }
    int64_t best = -1;
    for (int64_t j = 0; j < m; j++) {
        int64_t b = edges[j][0], c = edges[j][1];
        for (int64_t x = 0; x < kept[b]; x++) {
            int64_t a = near[start[b] + x];
            if (a == c) continue;
            for (int64_t y = 0; y < kept[c]; y++) {
                int64_t d = near[start[c] + y];
                if (d != a && d != b) {
                    int64_t total = scores[a] + scores[b] + scores[c] + scores[d];
                    if (total > best) best = total;
                }
            }
        }
    }
    free(degree);
    free(start);
    free(near);
    free(kept);
    return best;
}

static int64_t seed = 2242;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    static int64_t scores[N];
    static int64_t edges[N][2];
    int64_t check = 0;
    for (int g = 0; g < 40; g++) {
        for (int64_t i = 0; i < N; i++) scores[i] = wide_random() % 100000000 + 1;
        for (int64_t j = 0; j < N; j++) {
            edges[j][0] = j;
            edges[j][1] = (j + 1 + wide_random() % (N / 2 - 2)) % N;
        }
        check = (check * 31 + maximum_score(scores, (const int64_t(*)[2])edges, N, N)) % 1000000007;
    }
    printf("40 graphs of 50000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
