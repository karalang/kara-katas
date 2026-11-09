// LeetCode #2039: The Time When the Network Becomes Idle -- the ★ arm in C,
// the same algorithm and workload as network.kara: the adjacency built per
// call as growable lists, breadth-first search from the master with an
// array queue, then each server's last message and its reply. The joined
// pairs of the generator live in an open-addressing hash set.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t *items; int64_t len, cap; } List;

static void push(List *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = x;
}

static int64_t network_becomes_idle(const int64_t (*edges)[2], int64_t m, const int64_t *patience, int64_t n) {
    List *adjacent = calloc(n, sizeof(List));
    for (int64_t k = 0; k < m; k++) {
        push(&adjacent[edges[k][0]], edges[k][1]);
        push(&adjacent[edges[k][1]], edges[k][0]);
    }
    int64_t *hops = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) hops[i] = -1;
    hops[0] = 0;
    int64_t *queue = malloc(n * sizeof(int64_t));
    int64_t head = 0, tail = 0;
    queue[tail++] = 0;
    while (head < tail) {
        int64_t u = queue[head++];
        for (int64_t k = 0; k < adjacent[u].len; k++) {
            int64_t v = adjacent[u].items[k];
            if (hops[v] == -1) {
                hops[v] = hops[u] + 1;
                queue[tail++] = v;
            }
        }
    }
    int64_t idle = 0;
    for (int64_t i = 1; i < n; i++) {
        int64_t round_trip = 2 * hops[i];
        int64_t last_sent = (round_trip - 1) / patience[i] * patience[i];
        int64_t t = last_sent + round_trip + 1;
        if (t > idle) idle = t;
    }
    for (int64_t i = 0; i < n; i++) free(adjacent[i].items);
    free(adjacent);
    free(hops);
    free(queue);
    return idle;
}

static int64_t seed = 2039;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

enum { N = 100000, SLOTS = 1 << 18 };

typedef struct {
    int64_t (*edges)[2];
    int64_t m;
    int64_t *patience;
} Network;

static int set_add(int64_t *slots, int64_t key) {
    uint64_t h = ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 46;
    while (slots[h] != -1) {
        if (slots[h] == key) return 0;
        h = (h + 1) & (SLOTS - 1);
    }
    slots[h] = key;
    return 1;
}

static int set_has(const int64_t *slots, int64_t key) {
    uint64_t h = ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 46;
    while (slots[h] != -1) {
        if (slots[h] == key) return 1;
        h = (h + 1) & (SLOTS - 1);
    }
    return 0;
}

static Network random_network(int64_t n, int64_t reach, int64_t extra, int64_t top) {
    Network net;
    net.edges = malloc((n - 1 + extra) * sizeof(int64_t[2]));
    net.m = 0;
    int64_t *slots = malloc(SLOTS * sizeof(int64_t));
    for (int64_t i = 0; i < SLOTS; i++) slots[i] = -1;
    for (int64_t v = 1; v < n; v++) {
        int64_t hi = next_random();
        int64_t lo = next_random();
        int64_t r = reach < v ? reach : v;
        int64_t u = v - 1 - (hi * 32768 + lo) % r;
        net.edges[net.m][0] = u;
        net.edges[net.m][1] = v;
        net.m++;
        set_add(slots, u * N + v);
    }
    int64_t tries = 0;
    while (net.m < n - 1 + extra && tries < 4 * extra) {
        tries++;
        int64_t h1 = next_random(), l1 = next_random();
        int64_t a = (h1 * 32768 + l1) % n;
        int64_t h2 = next_random(), l2 = next_random();
        int64_t b = (h2 * 32768 + l2) % n;
        int64_t u = a < b ? a : b, v = a < b ? b : a;
        if (u != v && !set_has(slots, u * N + v)) {
            set_add(slots, u * N + v);
            net.edges[net.m][0] = u;
            net.edges[net.m][1] = v;
            net.m++;
        }
    }
    free(slots);
    net.patience = malloc(n * sizeof(int64_t));
    net.patience[0] = 0;
    for (int64_t i = 1; i < n; i++) net.patience[i] = next_random() % top + 1;
    return net;
}

int main(void) {
    const int64_t tops[4] = {100000, 3, 1000, 1};
    const int64_t reaches[4] = {100000, 2, 50, 1};
    Network networks[4];
    for (int r = 0; r < 4; r++) networks[r] = random_network(N, reaches[r], 1, tops[r]);
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int64_t r = 0; r < 4; r++) {
            int64_t at = (round * 7919 + r * 104729) % 99999 + 1;
            networks[r].patience[at] = networks[r].patience[at] % 7 + 1;
            int64_t answer = network_becomes_idle((const int64_t (*)[2])networks[r].edges, networks[r].m, networks[r].patience, N);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
