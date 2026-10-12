// Benchmark for #431: mirror of encode.kara (left child, right sibling).
// Binary nodes are malloc'd and freed once decoded, where the Kāra
// program's reference-counted nodes are freed when the binary tree is
// dropped; the source and decoded trees are freed after each round.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node **children;
    int64_t len, cap;
} Node;

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct { int64_t *items; int64_t len, cap; } List;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->len++] = v;
}

static void push_child(Node *n, Node *c) {
    if (n->len == n->cap) {
        n->cap = n->cap ? n->cap * 2 : 4;
        n->children = realloc(n->children, n->cap * sizeof *n->children);
    }
    n->children[n->len++] = c;
}

static TreeNode *encode_node(Node *node) {
    TreeNode *t = malloc(sizeof *t);
    t->val = node->val;
    t->left = t->right = NULL;
    TreeNode *prev = NULL;
    for (int64_t i = 0; i < node->len; i++) {
        TreeNode *c = encode_node(node->children[i]);
        if (prev) prev->right = c;
        else t->left = c;
        prev = c;
    }
    return t;
}

static Node *decode_node(TreeNode *t) {
    Node *n = malloc(sizeof *n);
    n->val = t->val;
    n->children = NULL;
    n->len = n->cap = 0;
    for (TreeNode *c = t->left; c; c = c->right) push_child(n, decode_node(c));
    return n;
}

static void free_node(Node *n) {
    for (int64_t i = 0; i < n->len; i++) free_node(n->children[i]);
    free(n->children);
    free(n);
}

static void free_tree(TreeNode *t) {
    while (t) {
        TreeNode *right = t->right;
        free_tree(t->left);
        free(t);
        t = right;
    }
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static Node *build_random(int64_t i, int64_t *vals, List *kids) {
    Node *n = malloc(sizeof *n);
    n->val = vals[i];
    n->len = n->cap = 0;
    n->children = NULL;
    for (int64_t j = 0; j < kids[i].len; j++) push_child(n, build_random(kids[i].items[j], vals, kids));
    return n;
}

static void fold(Node *node, int64_t *count, int64_t *checksum) {
    *count += 1;
    *checksum = (*checksum * 31 + node->val) % 1000000007;
    for (int64_t i = 0; i < node->len; i++) fold(node->children[i], count, checksum);
}

int main(int argc, char **argv) {
    int64_t n = 10000;
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 100;
    int64_t seed = 431;
    int64_t count = 0, checksum = 0;
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
        Node *root = build_random(0, vals, kids);
        TreeNode *bin = encode_node(root);
        Node *back = decode_node(bin);
        free_tree(bin);
        free_node(root);
        fold(back, &count, &checksum);
        free_node(back);
        for (int64_t i = 0; i < n; i++) free(kids[i].items);
        free(kids);
        free(vals);
    }
    printf("%lld rounds of %lld nodes: %lld decoded, checksum %lld\n", (long long)rounds, (long long)n, (long long)count, (long long)checksum);
    return 0;
}
