// LeetCode #1123: Lowest Common Ancestor of Deepest Leaves -- the bench, the
// same workload as lca_deepest_leaves.kara: the one-walk solution over 16
// trees of 10^4 nodes, built once, each round hanging one more node on every
// tree and solving it again.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t walk(TreeNode *node, TreeNode **ans) {
    if (!node) {
        *ans = NULL;
        return 0;
    }
    TreeNode *la, *ra;
    int64_t ld = walk(node->left, &la);
    int64_t rd = walk(node->right, &ra);
    if (ld == rd) {
        *ans = node;
        return ld + 1;
    }
    if (ld > rd) {
        *ans = la;
        return ld + 1;
    }
    *ans = ra;
    return rd + 1;
}

static TreeNode *lca_deepest_leaves(TreeNode *root) {
    TreeNode *ans;
    walk(root, &ans);
    return ans;
}

static int64_t seed = 1123;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int random_value(void) {
    int64_t a = next_random();
    int64_t b = next_random();
    return (int)((a * 32768 + b) % 100001);
}

typedef struct {
    TreeNode **nodes;
    size_t len, cap;
} Tree;

static TreeNode *new_node(int val) {
    TreeNode *n = malloc(sizeof *n);
    n->val = val;
    n->left = n->right = NULL;
    return n;
}

static void push(Tree *t, TreeNode *n) {
    if (t->len == t->cap) {
        t->cap = t->cap ? t->cap * 2 : 16;
        t->nodes = realloc(t->nodes, t->cap * sizeof *t->nodes);
    }
    t->nodes[t->len++] = n;
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
            TreeNode *answer = lca_deepest_leaves(trees[j].nodes[0]);
            total += answer->val;
            check = (check * 31 + answer->val) % 1000000007;
        }
    }
    printf("200 rounds over 16 trees of 10^4 nodes: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
