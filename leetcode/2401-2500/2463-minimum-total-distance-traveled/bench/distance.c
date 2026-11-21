// LeetCode #2463: Minimum Total Distance Traveled -- the bench, the ★ arm
// in C: a table over the sorted robots and factories, each factory either
// skipped or given the next run of robots up to its limit. The robots and
// factories are sorted by `qsort` into copies, as the other languages
// sort copies.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NONE 9000000000000000000LL
#define N 100
#define M 100

typedef struct {
    int64_t at, limit;
} Factory;

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int by_factory(const void *a, const void *b) {
    const Factory *x = a, *y = b;
    if (x->at != y->at) return (x->at > y->at) - (x->at < y->at);
    return (x->limit > y->limit) - (x->limit < y->limit);
}

static int64_t best[N + 1][M + 1];

static int64_t minimum_total_distance(const int64_t *robot, int64_t n, const Factory *factory, int64_t m) {
    int64_t robots[N];
    Factory factories[M];
    memcpy(robots, robot, sizeof(int64_t) * n);
    memcpy(factories, factory, sizeof(Factory) * m);
    qsort(robots, n, sizeof(int64_t), by_value);
    qsort(factories, m, sizeof(Factory), by_factory);
    for (int64_t i = 0; i <= n; i++)
        for (int64_t j = 0; j <= m; j++) best[i][j] = NONE;
    for (int64_t j = 0; j <= m; j++) best[n][j] = 0;
    for (int64_t j = m - 1; j >= 0; j--) {
        int64_t at = factories[j].at, limit = factories[j].limit;
        for (int64_t i = n - 1; i >= 0; i--) {
            int64_t least = best[i][j + 1], run = 0;
            int64_t most = limit < n - i ? limit : n - i;
            for (int64_t t = 1; t <= most; t++) {
                int64_t d = robots[i + t - 1] - at;
                run += d < 0 ? -d : d;
                if (best[i + t][j + 1] < NONE && run + best[i + t][j + 1] < least) least = run + best[i + t][j + 1];
            }
            best[i][j] = least;
        }
    }
    return best[0][0];
}

static int64_t seed = 2463;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static int seen(const int64_t *values, int64_t len, int64_t v) {
    for (int64_t i = 0; i < len; i++)
        if (values[i] == v) return 1;
    return 0;
}

// the robots and factories distinct, checked by a scan rather than a set
static void random_case(int64_t *robot, Factory *factory, int64_t top, int64_t cap) {
    int64_t len = 0;
    while (len < N) {
        int64_t p = wide_random() % (2 * top + 1) - top;
        if (!seen(robot, len, p)) robot[len++] = p;
    }
    int64_t places[M];
    len = 0;
    while (len < M) {
        int64_t p = wide_random() % (2 * top + 1) - top;
        if (!seen(places, len, p)) {
            places[len] = p;
            factory[len].at = p;
            factory[len].limit = next_random() % (cap + 1);
            len++;
        }
    }
    int64_t room = 0;
    for (int64_t j = 0; j < M; j++) room += factory[j].limit;
    for (int64_t j = 0; room < N; j++, room++) factory[j % M].limit++;
}

#define CASES 40

int main(void) {
    // 40 cases of 100 robots and 100 factories over 2 10^9 places, limits
    // up to 2, built once; then 72 passes, each raising one limit of every
    // case, chosen by the checksum so far, then answering every case and
    // folding the answer plus the pass into the checksum
    static int64_t robots[CASES][N];
    static Factory factories[CASES][M];
    for (int c = 0; c < CASES; c++) random_case(robots[c], factories[c], 1000000000, 2);
    int64_t check = 0;
    for (int64_t p = 0; p < 72; p++) {
        for (int64_t c = 0; c < CASES; c++) {
            factories[c][(check + c) % M].limit++;
            check = (check * 31 + minimum_total_distance(robots[c], N, factories[c], M) % 1000000007 + p) % 1000000007;
        }
    }
    printf("72 passes over 40 cases of 100 robots: checksum %lld\n", (long long)check);
    return 0;
}
