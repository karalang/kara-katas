// LeetCode #2008: Maximum Earnings From Taxi -- the ★ arm's benchmark, a
// mirror of taxi.kara. Each point's rides are a growable array, as a
// `Vec[Vec[..]]` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t start, end, tip; } Ride;
typedef struct { int64_t start, earned; } Leg;
typedef struct { Leg *data; int64_t len, cap; } Legs;

static int64_t max_taxi_earnings(int64_t n, const Ride *rides, int64_t m) {
    Legs *ending = calloc(n + 1, sizeof(Legs));
    for (int64_t i = 0; i < m; i++) {
        Legs *l = &ending[rides[i].end];
        if (l->len == l->cap) {
            l->cap = l->cap ? l->cap * 2 : 4;
            l->data = realloc(l->data, l->cap * sizeof(Leg));
        }
        l->data[l->len++] = (Leg){rides[i].start, rides[i].end - rides[i].start + rides[i].tip};
    }
    int64_t *best = calloc(n + 1, sizeof(int64_t));
    for (int64_t p = 2; p <= n; p++) {
        best[p] = best[p - 1];
        for (int64_t j = 0; j < ending[p].len; j++) {
            int64_t c = best[ending[p].data[j].start] + ending[p].data[j].earned;
            if (c > best[p]) best[p] = c;
        }
    }
    int64_t answer = best[n];
    for (int64_t p = 0; p <= n; p++) free(ending[p].data);
    free(ending);
    free(best);
    return answer;
}

static int64_t seed = 2008;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static Ride roads[80][5000];
    for (int a = 0; a < 80; a++) {
        for (int i = 0; i < 5000; i++) {
            int64_t length = next_random() % 100 + 1;
            int64_t start = next_random() % (9900 - length) + 1;
            roads[a][i] = (Ride){start, start + length, next_random() % 1001};
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t r = 0; r < 25; r++) {
        for (int a = 0; a < 80; a++) {
            int64_t answer = max_taxi_earnings(10000 - r * 4, roads[a], 5000);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
