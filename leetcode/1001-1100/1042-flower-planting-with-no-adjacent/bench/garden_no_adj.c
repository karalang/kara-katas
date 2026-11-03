// LeetCode #1042: Flower Planting With No Adjacent -- bench, C mirror of
// garden_no_adj.kara (greedy over the gardens in order). Each garden's
// neighbors are a growable array, as the Kāra arm's `Vec[Vec[i64]]` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} vec;

static void push(vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? 2 * v->cap : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
        if (!v->data) abort();
    }
    v->data[v->len++] = x;
}

static int64_t *garden_no_adj(int64_t n, const int64_t (*paths)[2], int64_t m) {
    vec *neighbors = calloc(n, sizeof(vec));
    for (int64_t i = 0; i < m; i++) {
        int64_t x = paths[i][0], y = paths[i][1];
        push(&neighbors[x - 1], y - 1);
        push(&neighbors[y - 1], x - 1);
    }
    int64_t *answer = calloc(n, sizeof(int64_t));
    for (int64_t garden = 0; garden < n; garden++) {
        int taken[5] = {0, 0, 0, 0, 0};
        for (int64_t j = 0; j < neighbors[garden].len; j++) {
            taken[answer[neighbors[garden].data[j]]] = 1;
        }
        int64_t flower = 1;
        while (taken[flower]) flower++;
        answer[garden] = flower;
    }
    for (int64_t i = 0; i < n; i++) free(neighbors[i].data);
    free(neighbors);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t random_paths(int64_t n, int64_t tries, int64_t *seed, int64_t (*paths)[2]) {
    int64_t (*joined)[3] = malloc(n * sizeof(*joined));
    int64_t *deg = calloc(n, sizeof(int64_t));
    int64_t m = 0;
    for (int64_t t = 0; t < tries; t++) {
        int64_t x = next_random(seed) % n;
        int64_t y = next_random(seed) % n;
        if (x == y || deg[x] >= 3 || deg[y] >= 3) continue;
        int seen = 0;
        for (int64_t j = 0; j < deg[x]; j++) seen |= joined[x][j] == y;
        if (seen) continue;
        joined[x][deg[x]++] = y;
        joined[y][deg[y]++] = x;
        paths[m][0] = x + 1;
        paths[m][1] = y + 1;
        m++;
    }
    free(joined);
    free(deg);
    return m;
}

int main(void) {
    const int64_t count = 10, n = 10000, rounds = 100;
    int64_t seed = 1042;
    int64_t (*gardens[10])[2];
    int64_t sizes[10];
    for (int64_t g = 0; g < count; g++) {
        gardens[g] = malloc(2 * n * sizeof(*gardens[g]));
        sizes[g] = random_paths(n, 4 * n, &seed, gardens[g]);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t *answer = garden_no_adj(n, (const int64_t (*)[2])gardens[g], sizes[g]);
            int64_t sum = 0;
            for (int64_t i = 0; i < n; i++) sum += answer[i];
            free(answer);
            total += sum;
            check = (check * 131 + sum) % 1000000007;
        }
    }
    printf("%lld gardens of %lld plots, %lld rounds: types sum to %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    for (int64_t g = 0; g < count; g++) free(gardens[g]);
    return 0;
}
