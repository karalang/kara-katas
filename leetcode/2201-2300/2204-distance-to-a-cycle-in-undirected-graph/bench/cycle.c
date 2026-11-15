// benchmark's C mirror of cycle.kara (LeetCode #2204, the ★ arm): leaves
// peeled by degree, then one breadth-first search from the cycle. Each
// node's neighbours are a growable array, as Kāra's `Vec[Vec[i64]]`, and
// the queues are arrays used front to back.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *a;
    int64_t len, cap;
} list_t;

static void list_push(list_t *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->a = realloc(l->a, sizeof(int64_t) * (size_t)l->cap);
    }
    l->a[l->len++] = v;
}

static int64_t *distance_to_cycle(int64_t n, const int64_t (*edges)[2]) {
    list_t *adj = calloc((size_t)n, sizeof(list_t));
    int64_t *degree = calloc((size_t)n, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        list_push(&adj[edges[i][0]], edges[i][1]);
        list_push(&adj[edges[i][1]], edges[i][0]);
        degree[edges[i][0]]++;
        degree[edges[i][1]]++;
    }
    int64_t *queue = malloc(sizeof(int64_t) * (size_t)n);
    int64_t head = 0, tail = 0;
    for (int64_t v = 0; v < n; v++)
        if (degree[v] == 1) queue[tail++] = v;
    char *peeled = calloc((size_t)n, 1);
    while (head < tail) {
        int64_t v = queue[head++];
        peeled[v] = 1;
        for (int64_t j = 0; j < adj[v].len; j++) {
            int64_t u = adj[v].a[j];
            if (--degree[u] == 1) queue[tail++] = u;
        }
    }
    int64_t *dist = malloc(sizeof(int64_t) * (size_t)n);
    head = tail = 0;
    for (int64_t v = 0; v < n; v++) {
        dist[v] = -1;
        if (!peeled[v]) {
            dist[v] = 0;
            queue[tail++] = v;
        }
    }
    while (head < tail) {
        int64_t v = queue[head++];
        for (int64_t j = 0; j < adj[v].len; j++) {
            int64_t u = adj[v].a[j];
            if (dist[u] < 0) {
                dist[u] = dist[v] + 1;
                queue[tail++] = u;
            }
        }
    }
    for (int64_t v = 0; v < n; v++) free(adj[v].a);
    free(adj);
    free(degree);
    free(queue);
    free(peeled);
    return dist;
}

static int64_t seed = 2204;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static void random_graph(int64_t n, int64_t ring, int64_t (*edges)[2]) {
    int64_t *order = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) order[i] = i;
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = wide_random() % (i + 1), t = order[i];
        order[i] = order[j];
        order[j] = t;
    }
    for (int64_t i = 0; i < ring; i++) {
        edges[i][0] = order[i];
        edges[i][1] = order[(i + 1) % ring];
    }
    for (int64_t i = ring; i < n; i++) {
        edges[i][0] = order[i];
        edges[i][1] = order[wide_random() % i];
    }
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = wide_random() % (i + 1);
        int64_t a = edges[i][0], b = edges[i][1];
        edges[i][0] = edges[j][0];
        edges[i][1] = edges[j][1];
        edges[j][0] = a;
        edges[j][1] = b;
    }
    for (int64_t i = 0; i < n; i++)
        if (next_random() % 2 == 1) {
            int64_t t = edges[i][0];
            edges[i][0] = edges[i][1];
            edges[i][1] = t;
        }
    free(order);
}

int main(void) {
    static int64_t graphs[6][100000][2];
    const int64_t rings[6] = {3, 10, 100, 1000, 10000, 100000};
    for (int g = 0; g < 6; g++) random_graph(100000, rings[g], graphs[g]);
    int64_t check = 0;
    for (int pass = 0; pass < 5; pass++)
        for (int g = 0; g < 6; g++) {
            int64_t *dist = distance_to_cycle(100000, (const int64_t (*)[2])graphs[g]);
            int64_t sum = 0;
            for (int64_t v = 0; v < 100000; v++) sum += dist[v];
            check = (check * 31 + sum + dist[50000]) % 1000000007;
            free(dist);
        }
    printf("5 passes over 6 graphs: checksum %lld\n", (long long)check);
    return 0;
}
