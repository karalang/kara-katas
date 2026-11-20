// LeetCode #1273 bench, in C: the ★ arm (the children listed from the
// parents, then a depth-first search returning each subtree's sum and the
// nodes it keeps) on 20 random trees of 10,000 nodes with values from -3
// to 3, drawn once, 60 rounds; every answer folded into a checksum.
// The children are a list per node, grown by doubling, as a `Vec` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} list;

static void push(list *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = x;
}

static void subtree(int64_t node, const list *children, const int64_t *value, int64_t *sum, int64_t *kept) {
    int64_t s = value[node], k = 1;
    for (int64_t i = 0; i < children[node].len; i++) {
        int64_t cs, ck;
        subtree(children[node].items[i], children, value, &cs, &ck);
        s += cs;
        k += ck;
    }
    if (s == 0) {
        *sum = 0;
        *kept = 0;
    } else {
        *sum = s;
        *kept = k;
    }
}

static int64_t delete_tree_nodes(int64_t nodes, const int64_t *parent, const int64_t *value) {
    list *children = calloc(nodes, sizeof(list));
    for (int64_t i = 1; i < nodes; i++) push(&children[parent[i]], i);
    int64_t sum, kept;
    subtree(0, children, value, &sum, &kept);
    for (int64_t i = 0; i < nodes; i++) free(children[i].items);
    free(children);
    return kept;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static void random_parents(int64_t n, int64_t reach, int64_t *seed, int64_t *parent) {
    int64_t *order = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) order[i] = i;
    for (int64_t i = n - 1; i >= 2; i--) {
        int64_t j = 1 + next_random(seed) % i;
        int64_t t = order[i];
        order[i] = order[j];
        order[j] = t;
    }
    parent[0] = -1;
    for (int64_t i = 1; i < n; i++) {
        int64_t back = 1 + next_random(seed) % (reach < i ? reach : i);
        parent[order[i]] = order[i - back];
    }
    free(order);
}

int main(void) {
    int64_t seed = 1273;
    static int64_t parents[20][10000], values[20][10000];
    for (int t = 0; t < 20; t++) {
        random_parents(10000, 1000, &seed, parents[t]);
        for (int i = 0; i < 10000; i++) values[t][i] = next_random(&seed) % 7 - 3;
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 60; round++)
        for (int t = 0; t < 20; t++)
            check = (check * 131 + delete_tree_nodes(10000, parents[t], values[t]) + round) % 1000000007;
    printf("60 rounds of 20 trees of 10000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
