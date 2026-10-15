// Benchmark for #652: a number for every shape, as the Kara ★ arm. The
// map from (value, left number, right number) to a number is an
// open-addressing table sized for the tree, made for each call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t v, l, r, id;
} Slot;

static Slot *table;
static uint64_t mask;
static int64_t *counts;
static int64_t ncounts;
static TreeNode **found;
static int64_t nfound;

static uint64_t mix(int64_t v, int64_t l, int64_t r) {
    uint64_t h = (uint64_t)v * 0x9E3779B97F4A7C15ull;
    h = (h ^ (uint64_t)l) * 0xBF58476D1CE4E5B9ull;
    h = (h ^ (uint64_t)r) * 0x94D049BB133111EBull;
    return h ^ (h >> 31);
}

static int64_t number(TreeNode *node) {
    if (!node) return 0;
    int64_t l = number(node->left);
    int64_t r = number(node->right);
    uint64_t i = mix(node->val, l, r) & mask;
    while (table[i].id && !(table[i].v == node->val && table[i].l == l && table[i].r == r))
        i = (i + 1) & mask;
    if (!table[i].id) {
        counts[ncounts++] = 0;
        table[i] = (Slot){node->val, l, r, ncounts};
    }
    int64_t id = table[i].id;
    if (++counts[id - 1] == 2) found[nfound++] = node;
    return id;
}

static int64_t find_duplicate_subtrees(TreeNode *root, int64_t size) {
    uint64_t cap = 1;
    while (cap < (uint64_t)size * 2) cap <<= 1;
    table = calloc(cap, sizeof *table);
    mask = cap - 1;
    counts = malloc(size * sizeof *counts);
    found = malloc(size * sizeof *found);
    ncounts = nfound = 0;
    number(root);
    free(table);
    free(counts);
    return nfound;
}

static int64_t seed = 652;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static TreeNode *leaf(int64_t v) {
    TreeNode *n = malloc(sizeof *n);
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

static TreeNode *random_tree(int64_t size, int64_t spread) {
    TreeNode *root = leaf(next_random() % spread);
    for (int64_t k = 1; k < size; k++) {
        TreeNode *c = leaf(next_random() % spread);
        TreeNode *node = root;
        for (;;) {
            if (next_random() % 2 == 0) {
                if (node->left) node = node->left;
                else { node->left = c; break; }
            } else {
                if (node->right) node = node->right;
                else { node->right = c; break; }
            }
        }
    }
    return root;
}

int main(void) {
    int inputs = 4, rounds = 40;
    int64_t spreads[] = {2, 3, 5, 401};
    TreeNode *trees[4];
    for (int i = 0; i < inputs; i++) trees[i] = random_tree(100000, spreads[i]);
    int64_t kinds = 0, checksum = 0;
    for (int r = 0; r < rounds; r++) {
        int64_t n = find_duplicate_subtrees(trees[r % inputs], 100000);
        kinds += n;
        for (int64_t k = 0; k < n; k++)
            checksum = (checksum * 31 + found[k]->val + 1) % 1000000007;
        free(found);
    }
    printf("%d trees, %d rounds: %lld kinds, checksum %lld\n", inputs, rounds,
           (long long)kinds, (long long)checksum);
    return 0;
}
