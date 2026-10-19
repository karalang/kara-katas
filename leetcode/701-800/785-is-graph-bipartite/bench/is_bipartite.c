// LeetCode 785 — Is Graph Bipartite?: the bench, in C.
// Mirrors is_bipartite.kara: two colours by breadth first search over the
// same 64 graphs, with a fresh colour array and queue for each.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->len++] = v;
}

static int is_bipartite(const List *graph, int64_t n) {
    int64_t *colour = malloc(n * sizeof *colour);
    int64_t *queue = malloc(n * sizeof *queue);
    for (int64_t i = 0; i < n; i++) colour[i] = -1;
    int ok = 1;
    for (int64_t start = 0; start < n && ok; start++) {
        if (colour[start] != -1) continue;
        colour[start] = 0;
        int64_t head = 0, tail = 0;
        queue[tail++] = start;
        while (head < tail && ok) {
            int64_t u = queue[head++];
            for (int64_t k = 0; k < graph[u].len; k++) {
                int64_t v = graph[u].items[k];
                if (colour[v] == -1) {
                    colour[v] = 1 - colour[u];
                    queue[tail++] = v;
                } else if (colour[v] == colour[u]) {
                    ok = 0;
                    break;
                }
            }
        }
    }
    free(colour);
    free(queue);
    return ok;
}

static int64_t seed = 785;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static List graphs[64][100];
    for (int g = 0; g < 64; g++) {
        int64_t side[100];
        for (int i = 0; i < 100; i++) side[i] = next_random() % 2;
        List *graph = graphs[g];
        for (int64_t a = 0; a < 100; a++)
            for (int64_t b = a + 1; b < 100; b++)
                if (side[a] != side[b] && next_random() % 10 == 0) {
                    push(&graph[a], b);
                    push(&graph[b], a);
                }
        if (g % 2 == 1) {
            int64_t a = next_random() % 100;
            int64_t b = (a + 1) % 100;
            while (side[b] != side[a]) b = (b + 1) % 100;
            push(&graph[a], b);
            push(&graph[b], a);
        }
    }
    const int64_t rounds = 500000;
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int answer = is_bipartite(graphs[r % 64], 100);
        if (answer) yes++;
        check = (check * 31 + (answer ? 2 : 1) + r % 7) % 1000000007;
    }
    printf("%lld rounds of 100-node graphs: %lld bipartite, checksum %lld\n",
           (long long)rounds, (long long)yes, (long long)check);
    return 0;
}
