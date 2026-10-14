// Benchmark for #617: the ★ arm (recursion, a new tree); see
// merge_trees.kara. A subtree only one tree has is shared by pointer, as
// the Kāra arm shares the `shared struct` node; each merge's new nodes
// are `malloc`'d one at a time and listed, and freed after the walk.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    TreeNode **items;
    size_t len, cap;
} Made;

static TreeNode *node_new(int64_t val, Made *made) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = val;
    n->left = n->right = NULL;
    if (made) {
        if (made->len == made->cap) {
            made->cap = made->cap ? 2 * made->cap : 64;
            made->items = realloc(made->items, made->cap * sizeof(TreeNode *));
        }
        made->items[made->len++] = n;
    }
    return n;
}

static TreeNode *merge_trees(TreeNode *root1, TreeNode *root2, Made *made) {
    if (root1 && root2) {
        TreeNode *n = node_new(root1->val + root2->val, made);
        n->left = merge_trees(root1->left, root2->left, made);
        n->right = merge_trees(root1->right, root2->right, made);
        return n;
    }
    return root1 ? root1 : root2;
}

// ---- benchmark --------------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *random_tree(int64_t size, int64_t lean, int64_t *seed) {
    TreeNode *root = node_new(next_random(seed) % 20001 - 10000, NULL);
    for (int64_t k = 1; k < size; k++) {
        TreeNode *c = node_new(next_random(seed) % 20001 - 10000, NULL);
        TreeNode *node = root;
        for (;;) {
            if (next_random(seed) % 100 < lean) {
                if (node->left) {
                    node = node->left;
                } else {
                    node->left = c;
                    break;
                }
            } else {
                if (node->right) {
                    node = node->right;
                } else {
                    node->right = c;
                    break;
                }
            }
        }
    }
    return root;
}

static void walk(TreeNode *node, int64_t *count, int64_t *h) {
    if (node) {
        *count += 1;
        *h = (*h * 31 + node->val + 20000) % 1000000007;
        walk(node->left, count, h);
        walk(node->right, count, h);
    }
}

int main(void) {
    enum { TREES = 20, ROUNDS = 10000 };
    int64_t seed = 617;
    static TreeNode *all[TREES];
    for (int t = 0; t < TREES; t++) {
        int64_t lean = 30 + next_random(&seed) % 41;
        all[t] = random_tree(2000, lean, &seed);
    }
    Made made = {0};
    int64_t count = 0, checksum = 0;
    for (int r = 0; r < ROUNDS; r++) {
        made.len = 0;
        TreeNode *merged = merge_trees(all[(r * 7) % TREES], all[(r * 3 + 1) % TREES], &made);
        walk(merged, &count, &checksum);
        for (size_t k = 0; k < made.len; k++) free(made.items[k]);
    }
    free(made.items);
    printf("%d trees, %d rounds: %lld nodes, checksum %lld\n", TREES, ROUNDS, (long long)count,
           (long long)checksum);
    return 0;
}
