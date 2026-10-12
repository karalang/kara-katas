// Benchmark for #429: mirror of level_order.kara (breadth first, a
// level at a time). The Kāra arm takes the tree by value and frees each
// level's nodes once their children have moved on; here each node is
// freed once visited.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node **children;
    int64_t len, cap;
} Node;

typedef struct { int64_t *items; int64_t len, cap; } List;
typedef struct { Node **items; int64_t len, cap; } Nodes;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->len++] = v;
}

static void push_node(Nodes *l, Node *v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->len++] = v;
}

typedef struct { List *rows; int64_t len, cap; } Levels;

static Levels level_order(Node *root) {
    Levels levels = {0};
    Nodes level = {0};
    if (root) push_node(&level, root);
    while (level.len > 0) {
        List row = {0};
        Nodes next = {0};
        for (int64_t i = 0; i < level.len; i++) {
            Node *node = level.items[i];
            push(&row, node->val);
            for (int64_t j = 0; j < node->len; j++) push_node(&next, node->children[j]);
            free(node->children);
            free(node);
        }
        if (levels.len == levels.cap) {
            levels.cap = levels.cap ? levels.cap * 2 : 4;
            levels.rows = realloc(levels.rows, levels.cap * sizeof *levels.rows);
        }
        levels.rows[levels.len++] = row;
        free(level.items);
        level = next;
    }
    free(level.items);
    return levels;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static Node *build_random(int64_t i, int64_t *vals, List *kids) {
    Node *n = malloc(sizeof *n);
    n->val = vals[i];
    n->len = n->cap = kids[i].len;
    n->children = malloc((n->cap ? n->cap : 1) * sizeof *n->children);
    for (int64_t j = 0; j < kids[i].len; j++) n->children[j] = build_random(kids[i].items[j], vals, kids);
    return n;
}

int main(int argc, char **argv) {
    int64_t n = 10000;
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 200;
    int64_t seed = 429;
    int64_t rows = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t reach = 10 + step(&seed) % 1000;
        int64_t *vals = malloc(n * sizeof *vals);
        List *kids = calloc(n, sizeof *kids);
        for (int64_t i = 0; i < n; i++) {
            vals[i] = step(&seed) % 10001;
            if (i > 0) {
                int64_t lim = i < reach ? i : reach;
                int64_t back = 1 + step(&seed) % lim;
                push(&kids[i - back], i);
            }
        }
        Levels levels = level_order(build_random(0, vals, kids));
        rows += levels.len;
        for (int64_t i = 0; i < levels.len; i++) {
            List row = levels.rows[i];
            checksum = (checksum * 31 + row.len * 10007 + row.items[0] + row.items[row.len - 1]) % 1000000007;
            free(row.items);
        }
        free(levels.rows);
        for (int64_t i = 0; i < n; i++) free(kids[i].items);
        free(kids);
        free(vals);
    }
    printf("%lld rounds of %lld nodes: %lld levels, checksum %lld\n", (long long)rounds, (long long)n, (long long)rows, (long long)checksum);
    return 0;
}
