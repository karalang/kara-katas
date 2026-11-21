// LeetCode #2458: Height of Binary Tree After Subtree Removal Queries --
// the bench, the ★ arm in C: every subtree's height, then a walk down
// carrying the height the tree keeps without each node. C has no hash
// map, so both are kept in open-addressing tables of 2^15 slots keyed by
// the value, cleared for every tree asked. The nodes are one malloc'd
// array linked by pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

#define CAP (1 << 15)

typedef struct {
    int64_t key, value;
} Slot;

typedef struct {
    Slot slots[CAP];
} Table;

static void clear(Table *t) {
    for (int i = 0; i < CAP; i++) t->slots[i].key = 0;
}

static Slot *find(Table *t, int64_t key) {
    uint64_t h = ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 49;
    while (t->slots[h].key != 0 && t->slots[h].key != key) h = (h + 1) & (CAP - 1);
    return &t->slots[h];
}

static void put(Table *t, int64_t key, int64_t value) {
    Slot *s = find(t, key);
    s->key = key;
    s->value = value;
}

static Table heights, answers;

static int64_t height(const TreeNode *node) {
    if (!node) return -1;
    int64_t l = height(node->left), r = height(node->right);
    int64_t h = 1 + (l > r ? l : r);
    put(&heights, node->val, h);
    return h;
}

static int64_t of(const TreeNode *node) {
    return node ? find(&heights, node->val)->value : -1;
}

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static void walk(const TreeNode *node, int64_t depth, int64_t rest) {
    if (!node) return;
    put(&answers, node->val, rest);
    walk(node->left, depth + 1, max64(rest, depth + 1 + of(node->right)));
    walk(node->right, depth + 1, max64(rest, depth + 1 + of(node->left)));
}

static void tree_queries(const TreeNode *root, const int64_t *queries, int64_t q, int64_t *out) {
    clear(&heights);
    height(root);
    clear(&answers);
    walk(root, 0, 0);
    for (int64_t i = 0; i < q; i++) out[i] = find(&answers, queries[i])->value;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2458;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *random_tree(TreeNode *nodes, int n) {
    int32_t *values = malloc(sizeof(int32_t) * n);
    for (int i = 0; i < n; i++) values[i] = i + 1;
    for (int i = n - 1; i >= 1; i--) {
        int j = (int)(next_random() % (i + 1));
        int32_t x = values[i];
        values[i] = values[j];
        values[j] = x;
    }
    for (int i = 0; i < n; i++) {
        nodes[i].val = values[i];
        nodes[i].left = nodes[i].right = NULL;
    }
    free(values);
    for (int k = 1; k < n; k++) {
        int64_t high = next_random();
        TreeNode *at = &nodes[(high * 32768 + next_random()) % k];
        for (;;) {
            if (next_random() % 2 == 0) {
                if (at->left) at = at->left;
                else { at->left = &nodes[k]; break; }
            } else {
                if (at->right) at = at->right;
                else { at->right = &nodes[k]; break; }
            }
        }
    }
    return &nodes[0];
}

int main(void) {
    // 20 random trees of 10^4 nodes built once; then 60 passes, each
    // asking every tree about every value but the root's, pass p starting
    // its queries p * 101 values along
    const int64_t n = 10000;
    TreeNode *nodes = malloc(sizeof(TreeNode) * n * 20);
    TreeNode *trees[20];
    for (int t = 0; t < 20; t++) trees[t] = random_tree(nodes + t * n, (int)n);
    int64_t *queries = malloc(sizeof(int64_t) * n);
    int64_t *out = malloc(sizeof(int64_t) * n);
    int64_t check = 0;
    for (int64_t p = 0; p < 60; p++) {
        for (int t = 0; t < 20; t++) {
            int64_t r = trees[t]->val, q = 0;
            for (int64_t i = 0; i < n; i++) {
                int64_t v = 1 + (i + p * 101) % n;
                if (v != r) queries[q++] = v;
            }
            tree_queries(trees[t], queries, q, out);
            for (int64_t i = 0; i < q; i++) check = (check * 31 + out[i] + p) % 1000000007;
        }
    }
    free(out);
    free(queries);
    free(nodes);
    printf("60 passes over 20 trees of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
