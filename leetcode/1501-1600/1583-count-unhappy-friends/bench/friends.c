// LeetCode #1583 bench: the same table of ranks, in C. Every list, rank row
// and pair is its own allocation, as in the Kara Vec[Vec[i64]]s.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t unhappy_friends(int64_t n, int64_t **preferences, int64_t **pairs) {
    int64_t **rank = malloc(n * sizeof(int64_t *));
    for (int64_t x = 0; x < n; x++) {
        rank[x] = calloc(n, sizeof(int64_t));
        for (int64_t r = 0; r < n - 1; r++) rank[x][preferences[x][r]] = r;
    }
    int64_t *partner = calloc(n, sizeof(int64_t));
    for (int64_t k = 0; k < n / 2; k++) {
        partner[pairs[k][0]] = pairs[k][1];
        partner[pairs[k][1]] = pairs[k][0];
    }
    int64_t unhappy = 0;
    for (int64_t x = 0; x < n; x++) {
        int64_t y = partner[x];
        for (int64_t i = 0; i < rank[x][y]; i++) {
            int64_t u = preferences[x][i];
            if (rank[u][x] < rank[u][partner[u]]) {
                unhappy++;
                break;
            }
        }
    }
    for (int64_t x = 0; x < n; x++) free(rank[x]);
    free(rank);
    free(partner);
    return unhappy;
}

static int64_t seed = 1583;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static int64_t *shuffled(int64_t n) {
    int64_t *v = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) v[i] = i;
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = next_random() % (i + 1);
        int64_t t = v[i];
        v[i] = v[j];
        v[j] = t;
    }
    return v;
}

int main(void) {
    enum { P = 40, N = 500 };
    int64_t **prefs[P], **pairs[P];
    for (int p = 0; p < P; p++) {
        prefs[p] = malloc(N * sizeof(int64_t *));
        for (int64_t x = 0; x < N; x++) {
            int64_t *order = shuffled(N);
            int64_t *list = malloc((N - 1) * sizeof(int64_t));
            int64_t k = 0;
            for (int64_t i = 0; i < N; i++)
                if (order[i] != x) list[k++] = order[i];
            free(order);
            prefs[p][x] = list;
        }
        int64_t *line = shuffled(N);
        pairs[p] = malloc(N / 2 * sizeof(int64_t *));
        for (int64_t k = 0; k < N / 2; k++) {
            pairs[p][k] = malloc(2 * sizeof(int64_t));
            pairs[p][k][0] = line[2 * k];
            pairs[p][k][1] = line[2 * k + 1];
        }
        free(line);
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < P; p++) {
        int64_t unhappy = unhappy_friends(N, prefs[p], pairs[p]);
        total += unhappy;
        check = mix(check, unhappy);
    }
    printf("40 problems of 500 friends: unhappy %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int p = 0; p < P; p++) {
        for (int64_t x = 0; x < N; x++) free(prefs[p][x]);
        for (int64_t k = 0; k < N / 2; k++) free(pairs[p][k]);
        free(prefs[p]);
        free(pairs[p]);
    }
    return 0;
}
