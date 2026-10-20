// Benchmark for #815: Bus Routes -- mirror of the ★ arm (breadth-first
// search over buses), with the same workload as bus_routes.kara. The map
// from stop to buses and the set of stops seen are open-addressing hash
// tables, sized for the city at hand and freed after each search.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t stop;
    int64_t *buses;
    int64_t len, cap;
    int used;
} Slot;

static uint64_t mix(int64_t key) {
    uint64_t x = (uint64_t)key;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

static Slot *find(Slot *table, size_t cap, int64_t stop) {
    size_t at = mix(stop) & (cap - 1);
    while (table[at].used && table[at].stop != stop) {
        at = (at + 1) & (cap - 1);
    }
    return &table[at];
}

// Inserts stop into the set; returns 1 if it was not there.
static int set_insert(int64_t *keys, char *used, size_t cap, int64_t stop) {
    size_t at = mix(stop) & (cap - 1);
    while (used[at]) {
        if (keys[at] == stop) {
            return 0;
        }
        at = (at + 1) & (cap - 1);
    }
    used[at] = 1;
    keys[at] = stop;
    return 1;
}

static int64_t num_buses_to_destination(int64_t **routes, const int64_t *lens, int64_t n,
                                        int64_t source, int64_t target) {
    if (source == target) {
        return 0;
    }
    int64_t stops = 0;
    for (int64_t b = 0; b < n; b++) {
        stops += lens[b];
    }
    size_t cap = 16;
    while (cap < 2 * (size_t)stops) {
        cap *= 2;
    }
    Slot *table = calloc(cap, sizeof(Slot));
    for (int64_t b = 0; b < n; b++) {
        for (int64_t j = 0; j < lens[b]; j++) {
            Slot *s = find(table, cap, routes[b][j]);
            if (!s->used) {
                s->used = 1;
                s->stop = routes[b][j];
            }
            if (s->len == s->cap) {
                s->cap = s->cap ? 2 * s->cap : 4;
                s->buses = realloc(s->buses, s->cap * sizeof(int64_t));
            }
            s->buses[s->len++] = b;
        }
    }
    int64_t answer = -1;
    Slot *first = find(table, cap, source);
    char *taken = calloc(n, 1);
    int64_t *queue_bus = malloc(n * sizeof(int64_t));
    int64_t *queue_count = malloc(n * sizeof(int64_t));
    int64_t *seen_keys = malloc(cap * sizeof(int64_t));
    char *seen_used = calloc(cap, 1);
    int64_t head = 0, tail = 0;
    if (first->used) {
        for (int64_t k = 0; k < first->len; k++) {
            taken[first->buses[k]] = 1;
            queue_bus[tail] = first->buses[k];
            queue_count[tail++] = 1;
        }
    }
    while (head < tail && answer < 0) {
        int64_t bus = queue_bus[head], count = queue_count[head++];
        for (int64_t j = 0; j < lens[bus]; j++) {
            int64_t stop = routes[bus][j];
            if (stop == target) {
                answer = count;
                break;
            }
            if (!set_insert(seen_keys, seen_used, cap, stop)) {
                continue;
            }
            Slot *s = find(table, cap, stop);
            for (int64_t k = 0; k < s->len; k++) {
                int64_t next = s->buses[k];
                if (!taken[next]) {
                    taken[next] = 1;
                    queue_bus[tail] = next;
                    queue_count[tail++] = count + 1;
                }
            }
        }
    }
    for (size_t at = 0; at < cap; at++) {
        free(table[at].buses);
    }
    free(table);
    free(taken);
    free(queue_bus);
    free(queue_count);
    free(seen_keys);
    free(seen_used);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 64, ROUTES = 100, STOPS = 20000 };
    const int64_t rounds = 4000;
    int64_t seed = 815;
    static int64_t *cities[COUNT][ROUTES];
    static int64_t lens[COUNT][ROUTES];
    char *on = calloc(STOPS, 1);
    for (int g = 0; g < COUNT; g++) {
        for (int b = 0; b < ROUTES; b++) {
            int64_t len = 1 + next_random(&seed) % 200;
            int64_t *route = malloc(len * sizeof(int64_t));
            int64_t have = 0;
            while (have < len) {
                int64_t stop = next_random(&seed) % STOPS;
                if (!on[stop]) {
                    on[stop] = 1;
                    route[have++] = stop;
                }
            }
            for (int64_t j = 0; j < len; j++) {
                on[route[j]] = 0;
            }
            cities[g][b] = route;
            lens[g][b] = len;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int g = (int)(round % COUNT);
        int64_t ends[2];
        for (int e = 0; e < 2; e++) {
            if (next_random(&seed) % 8 == 0) {
                ends[e] = next_random(&seed) % STOPS;
            } else {
                int64_t b = next_random(&seed) % ROUTES;
                ends[e] = cities[g][b][next_random(&seed) % lens[g][b]];
            }
        }
        int64_t answer = num_buses_to_destination(cities[g], lens[g], ROUTES, ends[0], ends[1]);
        total += answer;
        checksum = (checksum * 31 + answer + 2) % 1000000007;
    }
    printf("%lld rounds of %d routes: total %lld, checksum %lld\n", (long long)rounds, ROUTES,
           (long long)total, (long long)checksum);
    return 0;
}
