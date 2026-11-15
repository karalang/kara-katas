// LeetCode #1161: Maximum Level Sum of a Binary Tree -- the bench, the same
// workload as max_level_sum.kara: the ★ arm's level-by-level walk over 16
// trees of 10^4 nodes, built once, each round hanging one more node on
// every tree and solving it again. Each level's nodes go in a fresh
// `malloc`ed array, as the ★ arm's `next` is a fresh `Vec`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    TreeNode **nodes;
    size_t len, cap;
} Tree;

static void push(Tree *t, TreeNode *n) {
    if (t->len == t->cap) {
        t->cap = t->cap ? t->cap * 2 : 16;
        t->nodes = realloc(t->nodes, t->cap * sizeof *t->nodes);
    }
    t->nodes[t->len++] = n;
}

static int64_t max_level_sum(TreeNode *root) {
    Tree level = {0};
    if (root) push(&level, root);
    int64_t best = 0, best_sum = 0, depth = 0;
    while (level.len > 0) {
        depth++;
        int64_t sum = 0;
        Tree next = {0};
        for (size_t i = 0; i < level.len; i++) {
            TreeNode *node = level.nodes[i];
            sum += node->val;
            if (node->left) push(&next, node->left);
            if (node->right) push(&next, node->right);
        }
        if (best == 0 || sum > best_sum) {
            best = depth;
            best_sum = sum;
        }
        free(level.nodes);
        level = next;
    }
    free(level.nodes);
    return best;
}

static int64_t seed = 1161;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int random_value(void) {
    int64_t a = next_random();
    int64_t b = next_random();
    return (int)((a * 32768 + b) % 200001 - 100000);
}

static TreeNode *new_node(int val) {
    TreeNode *n = malloc(sizeof *n);
    n->val = val;
    n->left = n->right = NULL;
    return n;
}

static void grow(Tree *t) {
    TreeNode *c = new_node(random_value());
    for (;;) {
        TreeNode *at = t->nodes[next_random() % (int64_t)t->len];
        if (next_random() % 2 == 0) {
            if (!at->left) {
                at->left = c;
                break;
            }
        } else if (!at->right) {
            at->right = c;
            break;
        }
    }
    push(t, c);
}

int main(void) {
    Tree trees[16] = {0};
    for (int j = 0; j < 16; j++) {
        push(&trees[j], new_node(random_value()));
        for (int i = 1; i < 10000; i++) grow(&trees[j]);
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 200; round++) {
        for (int j = 0; j < 16; j++) {
            grow(&trees[j]);
            int64_t level = max_level_sum(trees[j].nodes[0]);
            total += level;
            check = (check * 31 + level) % 1000000007;
        }
    }
    printf("200 rounds over 16 trees of 10^4 nodes: levels total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
