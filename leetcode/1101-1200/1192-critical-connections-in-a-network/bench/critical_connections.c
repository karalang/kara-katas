// LeetCode #1192 bench: the ★ arm in C, over the same 4 networks and 10
// rounds as the Kāra bench. Each call builds the adjacency as one vector of
// (neighbour, connection) pairs per server, grown by doubling, as a Vec is.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    long v, id;
} Arc;

typedef struct {
    Arc *data;
    long len, cap;
} Arcs;

static void arcs_push(Arcs *a, long v, long id) {
    if (a->len == a->cap) {
        a->cap = a->cap ? a->cap * 2 : 4;
        a->data = realloc(a->data, a->cap * sizeof(Arc));
    }
    a->data[a->len++] = (Arc){v, id};
}

typedef struct {
    long u, via, next;
} Frame;

typedef struct {
    long *data;
    long len, cap;
} Longs;

static void longs_push(Longs *a, long x) {
    if (a->len == a->cap) {
        a->cap = a->cap ? a->cap * 2 : 16;
        a->data = realloc(a->data, a->cap * sizeof(long));
    }
    a->data[a->len++] = x;
}

// The critical connections as pairs, two longs each, in `out`.
static void critical_connections(long n, const long *edges, long m, Longs *out) {
    Arcs *adj = calloc(n, sizeof(Arcs));
    for (long id = 0; id < m; id++) {
        long a = edges[2 * id], b = edges[2 * id + 1];
        arcs_push(&adj[a], b, id);
        arcs_push(&adj[b], a, id);
    }
    long *disc = malloc(n * sizeof(long));
    long *low = calloc(n, sizeof(long));
    for (long i = 0; i < n; i++) {
        disc[i] = -1;
    }
    disc[0] = 0;
    long time = 1;
    Frame *stack = malloc(n * sizeof(Frame));
    long top = 0;
    stack[top++] = (Frame){0, -1, 0};
    while (top > 0) {
        Frame *f = &stack[top - 1];
        long u = f->u;
        if (f->next < adj[u].len) {
            Arc arc = adj[u].data[f->next++];
            if (arc.id == f->via) {
                continue;
            }
            if (disc[arc.v] == -1) {
                disc[arc.v] = time;
                low[arc.v] = time;
                time++;
                stack[top++] = (Frame){arc.v, arc.id, 0};
            } else if (disc[arc.v] < low[u]) {
                low[u] = disc[arc.v];
            }
        } else {
            top--;
            if (top > 0) {
                long p = stack[top - 1].u;
                if (low[u] < low[p]) {
                    low[p] = low[u];
                }
                if (low[u] > disc[p]) {
                    longs_push(out, p);
                    longs_push(out, u);
                }
            }
        }
    }
    for (long i = 0; i < n; i++) {
        free(adj[i].data);
    }
    free(adj);
    free(disc);
    free(low);
    free(stack);
}

static long seed = 1192;

static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648L;
    return seed / 65536;
}

// An open-addressing set of joined pairs, for building the networks.
typedef struct {
    long *keys;
    long cap;
} PairSet;

static int pairset_insert(PairSet *s, long a, long b) {
    long key = a * 1000003 + b + 1;
    unsigned long h = (unsigned long)key * 0x9E3779B97F4A7C15UL;
    long i = (long)(h % (unsigned long)s->cap);
    while (s->keys[i] != 0) {
        if (s->keys[i] == key) {
            return 0;
        }
        i = (i + 1) % s->cap;
    }
    s->keys[i] = key;
    return 1;
}

static long random_network(long n, long extra, long **out) {
    PairSet joined = {calloc(1 << 19, sizeof(long)), 1 << 19};
    long *edges = malloc(2 * (n - 1 + extra) * sizeof(long));
    long m = 0;
    for (long v = 1; v < n; v++) {
        long u = next_random() % v;
        pairset_insert(&joined, u, v);
        edges[2 * m] = u;
        edges[2 * m + 1] = v;
        m++;
    }
    for (long k = 0; k < extra; k++) {
        long a = next_random() % n;
        long b = next_random() % n;
        long lo = a < b ? a : b, hi = a < b ? b : a;
        if (a != b && pairset_insert(&joined, lo, hi)) {
            edges[2 * m] = a;
            edges[2 * m + 1] = b;
            m++;
        }
    }
    free(joined.keys);
    *out = edges;
    return m;
}

int main(void) {
    long ns[4] = {50000, 100000, 100000, 100000};
    long *edges[4];
    long ms[4];
    ms[0] = random_network(50000, 50001, &edges[0]);
    ms[1] = random_network(100000, 0, &edges[1]);
    edges[2] = malloc(2 * 99999 * sizeof(long));
    edges[3] = malloc(2 * 100000 * sizeof(long));
    for (long i = 0; i < 99999; i++) {
        edges[2][2 * i] = edges[3][2 * i] = i;
        edges[2][2 * i + 1] = edges[3][2 * i + 1] = i + 1;
    }
    edges[3][2 * 99999] = 99999;
    edges[3][2 * 99999 + 1] = 0;
    ms[2] = 99999;
    ms[3] = 100000;
    long check = 0;
    for (int r = 0; r < 10; r++) {
        for (int k = 0; k < 4; k++) {
            Longs out = {NULL, 0, 0};
            critical_connections(ns[k], edges[k], ms[k], &out);
            check = (check * 131 + out.len / 2) % 1000000007;
            for (long i = 0; i < out.len; i += 2) {
                check = (check * 131 + out.data[i] * 100003 + out.data[i + 1]) % 1000000007;
            }
            free(out.data);
        }
    }
    printf("10 rounds of 4 networks of up to 100000 servers: checksum %ld\n", check);
    for (int k = 0; k < 4; k++) {
        free(edges[k]);
    }
    return 0;
}
