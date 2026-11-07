// LeetCode #1059: All Paths from Source Lead to Destination -- the
// benchmark, the same algorithm as paths.kara. The adjacency lists are
// growable arrays, as a Vec of Vecs is.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { UNSEEN = 0, ON_PATH = 1, DONE = 2 };

typedef struct { int64_t *items; int64_t len, cap; } list;
typedef struct { int64_t u, v; } edge;
typedef struct { edge *items; int64_t len, cap; } edges_t;
typedef struct { int64_t node, next; } frame;

static void push(list *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->len++] = x;
}

static bool leads_to_destination(int64_t n, const edges_t *edges, int64_t source, int64_t destination) {
    list *adj = calloc(n, sizeof *adj);
    for (int64_t i = 0; i < edges->len; i++) push(&adj[edges->items[i].u], edges->items[i].v);
    int64_t *state = calloc(n, sizeof *state);
    frame *stack = malloc(4 * sizeof *stack);
    int64_t len = 0, cap = 4;
    stack[len++] = (frame){source, 0};
    state[source] = ON_PATH;
    bool answer = true;
    while (len > 0) {
        int64_t top = len - 1;
        int64_t u = stack[top].node, next = stack[top].next;
        if (adj[u].len == 0 && u != destination) { answer = false; break; }
        if (next == adj[u].len) { state[u] = DONE; len--; continue; }
        stack[top].next = next + 1;
        int64_t v = adj[u].items[next];
        if (state[v] == ON_PATH) { answer = false; break; }
        if (state[v] == UNSEEN) {
            state[v] = ON_PATH;
            if (len == cap) { cap *= 2; stack = realloc(stack, cap * sizeof *stack); }
            stack[len++] = (frame){v, 0};
        }
    }
    for (int64_t i = 0; i < n; i++) free(adj[i].items);
    free(adj);
    free(state);
    free(stack);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void add(edges_t *e, int64_t u, int64_t v) {
    if (e->len == e->cap) {
        e->cap = e->cap ? e->cap * 2 : 4;
        e->items = realloc(e->items, e->cap * sizeof *e->items);
    }
    e->items[e->len++] = (edge){u, v};
}

static edges_t leaning_graph(int64_t n, int64_t per_node, int64_t back, int64_t *seed) {
    edges_t e = {0};
    for (int64_t u = 0; u < n - 1; u++) {
        int64_t k = next_random(seed) % (per_node + 1);
        for (int64_t i = 0; i < k; i++) {
            int64_t span = n - 1 - u < 20 ? n - 1 - u : 20;
            add(&e, u, u + 1 + next_random(seed) % span);
        }
        if (k == 0 && next_random(seed) % 4 != 0) add(&e, u, n - 1);
        if (next_random(seed) % back == 0) add(&e, u, next_random(seed) % (u + 1));
    }
    return e;
}

int main(void) {
    int64_t seed = 1059, n = 2000;
    edges_t graphs[20];
    for (int g = 0; g < 20; g++) graphs[g] = leaning_graph(n, 2, 1000, &seed);
    int64_t calls = 0, yes = 0, check = 0;
    for (int g = 0; g < 20; g++) {
        for (int64_t source = 0; source < n; source++) {
            bool answer = leads_to_destination(n, &graphs[g], source, n - 1);
            if (answer) yes++;
            check = (check * 31 + (answer ? 7 + source % 13 : 3)) % 1000000007;
            calls++;
        }
    }
    printf("%lld calls: %lld lead, checksum %lld\n", (long long)calls, (long long)yes, (long long)check);
    return 0;
}
