// LeetCode #1676: Lowest Common Ancestor of a Binary Tree IV -- the bench's
// C mirror: the ★ arm on one tree of 10000 nodes asked about 500 sets of 1
// to 50 nodes, all drawn first, each asked 10 times. Nodes are malloc'd
// one by one; the values go in an open-addressing hash set written for the
// bench, rebuilt for each set.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 10000
#define QUERIES 500
#define ROUNDS 10
#define MOST 50

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

// a set of at most MOST values: 128 slots, linear probing, -1 empty
typedef struct {
    int32_t slots[128];
} Set;

static void set_clear(Set *s) { memset(s->slots, 0xff, sizeof s->slots); }

static uint32_t set_hash(int32_t v) { return ((uint32_t)v * 2654435761u) >> 25; }

static void set_insert(Set *s, int32_t v) {
    uint32_t i = set_hash(v);
    while (s->slots[i] != -1 && s->slots[i] != v) i = (i + 1) & 127;
    s->slots[i] = v;
}

static int set_contains(const Set *s, int32_t v) {
    uint32_t i = set_hash(v);
    while (s->slots[i] != -1) {
        if (s->slots[i] == v) return 1;
        i = (i + 1) & 127;
    }
    return 0;
}

static TreeNode *search(TreeNode *node, const Set *wanted) {
    if (node == NULL) return NULL;
    if (set_contains(wanted, node->val)) return node;
    TreeNode *left = search(node->left, wanted);
    TreeNode *right = search(node->right, wanted);
    if (left != NULL && right != NULL) return node;
    return left != NULL ? left : right;
}

static TreeNode *lowest_common_ancestor(TreeNode *root, TreeNode **nodes, int64_t k) {
    Set wanted;
    set_clear(&wanted);
    for (int64_t i = 0; i < k; i++) set_insert(&wanted, nodes[i]->val);
    return search(root, &wanted);
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1676;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t values[N];
    static TreeNode *nodes[N];
    for (int64_t i = 0; i < N; i++) values[i] = (int32_t)i;
    for (int64_t i = N - 1; i >= 1; i--) {
        int64_t j = next_random() % (i + 1);
        int32_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    for (int64_t i = 0; i < N; i++) {
        TreeNode *node = malloc(sizeof *node);
        node->val = values[i];
        node->left = node->right = NULL;
        if (i > 0) {
            TreeNode *at = nodes[next_random() % i];
            for (;;) {
                if (next_random() % 2 == 0) {
                    if (at->left != NULL) at = at->left;
                    else { at->left = node; break; }
                } else {
                    if (at->right != NULL) at = at->right;
                    else { at->right = node; break; }
                }
            }
        }
        nodes[i] = node;
    }
    TreeNode *root = nodes[0];
    static TreeNode *sets[QUERIES][MOST];
    static int64_t sizes[QUERIES];
    for (int q = 0; q < QUERIES; q++) {
        int64_t k = next_random() % MOST + 1;
        for (int64_t i = 0; i < k; i++) {
            int64_t j = i + next_random() % (N - i);
            TreeNode *t = nodes[i];
            nodes[i] = nodes[j];
            nodes[j] = t;
        }
        memcpy(sets[q], nodes, (size_t)k * sizeof nodes[0]);
        sizes[q] = k;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int q = 0; q < QUERIES; q++) {
            int64_t found = lowest_common_ancestor(root, sets[q], sizes[q])->val;
            total += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    printf("%d nodes, %d sets, %d rounds: answers sum to %lld, checksum %lld\n", N, QUERIES, ROUNDS, (long long)total, (long long)check);
    for (int64_t i = 0; i < N; i++) free(nodes[i]);
    return 0;
}
