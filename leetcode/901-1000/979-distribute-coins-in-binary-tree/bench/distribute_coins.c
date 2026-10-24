// Benchmark: LeetCode #979 Distribute Coins in Binary Tree -- the ★ arm,
// excess from the leaves, on random trees of 100 nodes, LeetCode's
// largest. Mirrors distribute_coins.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t excess(TreeNode *t, int64_t *moves) {
    if (t == NULL) return 0;
    int64_t l = excess(t->left, moves);
    int64_t r = excess(t->right, moves);
    *moves += llabs(l) + llabs(r);
    return t->val + l + r - 1;
}

static int64_t distribute_coins(TreeNode *root) {
    int64_t moves = 0;
    excess(root, &moves);
    return moves;
}

static int64_t seed = 979;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(void) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = 0;
    t->left = NULL;
    t->right = NULL;
    return t;
}

static TreeNode *random_tree(int n) {
    TreeNode **nodes = malloc(sizeof(TreeNode *) * (size_t)n);
    nodes[0] = new_node();
    for (int i = 1; i < n; i++) {
        TreeNode *node = new_node(), *cur = nodes[0];
        for (;;) {
            if (next_random() % 2 == 0) {
                if (cur->left) cur = cur->left;
                else { cur->left = node; break; }
            } else {
                if (cur->right) cur = cur->right;
                else { cur->right = node; break; }
            }
        }
        nodes[i] = node;
    }
    for (int i = 0; i < n; i++) nodes[next_random() % n]->val++;
    TreeNode *root = nodes[0];
    free(nodes);
    return root;
}

int main(void) {
    int rounds = 200;
    static TreeNode *trees[2000];
    for (int i = 0; i < 2000; i++) trees[i] = random_tree(100);
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 2000; i++) {
            int64_t m = distribute_coins(trees[(r + i) % 2000]);
            total += m;
            check = (check * 31 + m + i) % 1000000007;
        }
    }
    printf("%d rounds over 2000 trees of 100 nodes: %lld moves, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
