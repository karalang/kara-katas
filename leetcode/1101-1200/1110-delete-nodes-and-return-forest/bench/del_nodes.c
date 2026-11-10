// LeetCode #1110: Delete Nodes And Return Forest -- the bench in C: the
// ★ arm over the same 16 trees of 1000 nodes and the same rounds. Each
// node is its own malloc, freed after its call; the values to delete go
// in an open-addressing table with a multiplicative hash and linear
// probing, built per call as Kāra's Set is.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int32_t *slots;  // 0 is empty: values are 1 to 1000
    size_t mask;
} Set;

static size_t slot_of(const Set *s, int32_t v) {
    size_t i = ((uint32_t)v * 2654435769u) & s->mask;
    while (s->slots[i] != 0 && s->slots[i] != v) i = (i + 1) & s->mask;
    return i;
}

static void set_init(Set *s, size_t n) {
    size_t cap = 16;
    while (cap < 2 * n) cap *= 2;
    s->slots = calloc(cap, sizeof(int32_t));
    s->mask = cap - 1;
}

static bool set_contains(const Set *s, int32_t v) { return s->slots[slot_of(s, v)] == v; }

typedef struct {
    TreeNode **items;
    size_t len, cap;
} Roots;

static void push(Roots *r, TreeNode *n) {
    if (r->len == r->cap) {
        r->cap = r->cap ? 2 * r->cap : 4;
        r->items = realloc(r->items, r->cap * sizeof(TreeNode *));
    }
    r->items[r->len++] = n;
}

static TreeNode *prune(TreeNode *n, bool parent_gone, const Set *gone, Roots *roots) {
    if (!n) return NULL;
    bool deleted = set_contains(gone, n->val);
    if (parent_gone && !deleted) push(roots, n);
    n->left = prune(n->left, deleted, gone, roots);
    n->right = prune(n->right, deleted, gone, roots);
    return deleted ? NULL : n;
}

static Roots del_nodes(TreeNode *root, const int32_t *to_delete, size_t m) {
    Set gone;
    set_init(&gone, m);
    for (size_t i = 0; i < m; i++) gone.slots[slot_of(&gone, to_delete[i])] = to_delete[i];
    Roots roots = {0};
    prune(root, true, &gone, &roots);
    free(gone.slots);
    return roots;
}

static int64_t seed = 1110;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    int32_t values[1000];
    int64_t left[1000], right[1000];
} Shape;

static void shape(Shape *s) {
    for (int i = 0; i < 1000; i++) s->values[i] = i + 1;
    for (int64_t i = 0; i < 1000; i++) {
        int64_t j = i + next_random() % (1000 - i);
        int32_t t = s->values[i];
        s->values[i] = s->values[j];
        s->values[j] = t;
    }
    for (int i = 0; i < 1000; i++) s->left[i] = s->right[i] = -1;
    for (int64_t k = 1; k < 1000; k++) {
        for (;;) {
            int64_t at = next_random() % k;
            if (next_random() % 2 == 0) {
                if (s->left[at] < 0) {
                    s->left[at] = k;
                    break;
                }
            } else if (s->right[at] < 0) {
                s->right[at] = k;
                break;
            }
        }
    }
}

static void build(const Shape *s, TreeNode **nodes) {
    for (int k = 0; k < 1000; k++) {
        nodes[k] = malloc(sizeof(TreeNode));
        nodes[k]->val = s->values[k];
        nodes[k]->left = nodes[k]->right = NULL;
    }
    for (int k = 0; k < 1000; k++) {
        if (s->left[k] >= 0) nodes[k]->left = nodes[s->left[k]];
        if (s->right[k] >= 0) nodes[k]->right = nodes[s->right[k]];
    }
}

int main(void) {
    static Shape shapes[16];
    for (int i = 0; i < 16; i++) shape(&shapes[i]);
    TreeNode *nodes[1000];
    int32_t to_delete[1000];
    int64_t trees = 0, check = 0;
    for (int round = 0; round < 200; round++) {
        for (int j = 0; j < 16; j++) {
            int third = (round + j) % 3;
            size_t m = 0;
            for (int32_t v = 1; v <= 1000; v++)
                if (v % 3 == third) to_delete[m++] = v;
            build(&shapes[j], nodes);
            Roots roots = del_nodes(nodes[0], to_delete, m);
            trees += roots.len;
            for (size_t i = 0; i < roots.len; i++) check = (check * 31 + roots.items[i]->val) % 1000000007;
            free(roots.items);
            for (int k = 0; k < 1000; k++) free(nodes[k]);
        }
    }
    printf("200 rounds over 16 trees of 1000 nodes: %lld trees, checksum %lld\n", (long long)trees, (long long)check);
    return 0;
}
