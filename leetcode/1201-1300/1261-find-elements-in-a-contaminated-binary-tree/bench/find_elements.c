// LeetCode #1261 bench, in C: the ★ arm (the tree recovered from the
// root down, every value kept in a hash set) on 20 random contaminated trees
// of 10000 nodes, at most 20 levels deep, built once; 120 rounds, each tree
// recovered again and asked 10000 targets, half of them nodes' places;
// the targets found counted and folded into a checksum. The set is
// open-addressed and rebuilt for every recovery, as the other languages'
// sets are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct { int64_t *keys; uint8_t *used; size_t cap, len; } Set;

static size_t mix(int64_t k) { uint64_t x = (uint64_t)k * 0x9E3779B97F4A7C15ULL; return (size_t)(x ^ (x >> 29)); }

static void set_init(Set *s, size_t cap) { s->cap = cap; s->len = 0; s->keys = malloc(cap * sizeof(int64_t)); s->used = calloc(cap, 1); }

static void set_free(Set *s) { free(s->keys); free(s->used); }

static size_t set_slot(const Set *s, int64_t k) {
    size_t i = mix(k) & (s->cap - 1);
    while (s->used[i] && s->keys[i] != k) i = (i + 1) & (s->cap - 1);
    return i;
}

static void set_add(Set *s, int64_t k) {
    if ((s->len + 1) * 2 > s->cap) {
        Set n; set_init(&n, s->cap * 2);
        for (size_t i = 0; i < s->cap; i++)
            if (s->used[i]) { size_t j = set_slot(&n, s->keys[i]); n.used[j] = 1; n.keys[j] = s->keys[i]; n.len++; }
        set_free(s); *s = n;
    }
    size_t i = set_slot(s, k);
    if (!s->used[i]) { s->used[i] = 1; s->keys[i] = k; s->len++; }
}

static int set_has(const Set *s, int64_t k) { return s->used[set_slot(s, k)]; }

static void recover(TreeNode *node, int64_t value, Set *values) {
    if (node) {
        node->val = value;
        set_add(values, value);
        recover(node->left, 2 * value + 1, values);
        recover(node->right, 2 * value + 2, values);
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static TreeNode *build(const Set *present, int64_t at) {
    if (!set_has(present, at)) return NULL;
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = -1;
    n->left = build(present, 2 * at + 1);
    n->right = build(present, 2 * at + 2);
    return n;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int64_t seed = 1261;
    TreeNode *trees[20];
    int64_t *targets[20];
    for (int t = 0; t < 20; t++) {
        int64_t *places = malloc(10000 * sizeof(int64_t));
        size_t n = 1; places[0] = 0;
        Set present; set_init(&present, 16); set_add(&present, 0);
        while (n < 10000) {
            int64_t p = places[next_random(&seed) % (int64_t)n];
            int64_t child = 2 * p + 1 + next_random(&seed) % 2;
            if (child < 2097151 && !set_has(&present, child)) { set_add(&present, child); places[n++] = child; }
        }
        qsort(places, n, sizeof(int64_t), cmp);
        int64_t deepest = places[n - 1];
        trees[t] = build(&present, 0);
        targets[t] = malloc(10000 * sizeof(int64_t));
        for (int q = 0; q < 10000; q++)
            targets[t][q] = q % 2 == 0 ? places[next_random(&seed) % 10000] : next_random(&seed) * 64 % (deepest + 1);
        set_free(&present); free(places);
    }
    long found = 0;
    int64_t check = 0;
    for (int r = 0; r < 120; r++)
        for (int t = 0; t < 20; t++) {
            Set values; set_init(&values, 16);
            recover(trees[t], 0, &values);
            for (int q = 0; q < 10000; q++)
                if (set_has(&values, targets[t][q])) { found++; check = (check * 131 + targets[t][q]) % 1000000007; }
            set_free(&values);
        }
    printf("120 rounds of 20 trees of 10000 nodes: %ld found, checksum %lld\n", found, (long long)check);
    return 0;
}
