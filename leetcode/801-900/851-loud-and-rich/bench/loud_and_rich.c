// Benchmark for #851: Loud and Rich -- C twin of the Kāra ★ arm (memoised
// search up the richer-than graph).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, sizeof(int64_t) * l->cap);
    }
    l->items[l->len++] = v;
}

static int64_t answer_for(int64_t x, const List *richer_than, const int64_t *quiet, int64_t *answer) {
    if (answer[x] < 0) {
        int64_t best = x;
        for (int64_t k = 0; k < richer_than[x].len; k++) {
            int64_t candidate = answer_for(richer_than[x].items[k], richer_than, quiet, answer);
            if (quiet[candidate] < quiet[best]) best = candidate;
        }
        answer[x] = best;
    }
    return answer[x];
}

static int64_t *loud_and_rich(const int64_t (*richer)[2], int64_t m, const int64_t *quiet, int64_t n) {
    List *richer_than = calloc(n, sizeof(List));
    for (int64_t k = 0; k < m; k++) push(&richer_than[richer[k][1]], richer[k][0]);
    int64_t *answer = malloc(sizeof(int64_t) * n);
    for (int64_t x = 0; x < n; x++) answer[x] = -1;
    for (int64_t x = 0; x < n; x++) answer_for(x, richer_than, quiet, answer);
    for (int64_t x = 0; x < n; x++) free(richer_than[x].items);
    free(richer_than);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

#define N 500

int main(void) {
    const int64_t count = 64, rounds = 10000, n = N;
    int64_t seed = 851;
    static int64_t (*richers[64])[2];
    static int64_t sizes[64];
    static int64_t quiets[64][N];
    for (int64_t g = 0; g < count; g++) {
        int64_t odds = 2LL << (g % 8);
        int64_t rank[N];
        for (int64_t i = 0; i < n; i++) rank[i] = i;
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            int64_t t = rank[i]; rank[i] = rank[j]; rank[j] = t;
        }
        int64_t cap = 1024, m = 0;
        int64_t (*richer)[2] = malloc(sizeof(int64_t[2]) * cap);
        for (int64_t i = 0; i < n; i++)
            for (int64_t j = i + 1; j < n; j++)
                if (next_random(&seed) % 1000 < odds) {
                    if (m == cap) {
                        cap *= 2;
                        richer = realloc(richer, sizeof(int64_t[2]) * cap);
                    }
                    richer[m][0] = rank[i];
                    richer[m][1] = rank[j];
                    m++;
                }
        richers[g] = richer;
        sizes[g] = m;
        for (int64_t i = 0; i < n; i++) quiets[g][i] = i;
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            int64_t t = quiets[g][i]; quiets[g][i] = quiets[g][j]; quiets[g][j] = t;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        int64_t *answer = loud_and_rich((const int64_t (*)[2])richers[g], sizes[g], quiets[g], n);
        for (int64_t x = 0; x < n; x++) {
            total += quiets[g][answer[x]];
            checksum = (checksum * 31 + answer[x]) % 1000000007;
        }
        free(answer);
    }
    printf("%lld rounds of %lld cases: quietness sums to %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
