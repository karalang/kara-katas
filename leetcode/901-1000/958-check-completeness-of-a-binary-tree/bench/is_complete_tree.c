// Benchmark: LeetCode #958 Check Completeness of a Binary Tree -- the ★
// arm, the first gap, on trees of 100 nodes, LeetCode's largest. Mirrors
// is_complete_tree.kara, .rs, .py and go-seq/. The queue is a ring of
// node pointers on the stack, a gap as NULL; a tree of n nodes queues at
// most 2n + 1 entries.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static bool is_complete_tree(TreeNode *root) {
    TreeNode *queue[256];
    int head = 0, tail = 0;
    queue[tail++] = root;
    bool gap = false;
    while (head < tail) {
        TreeNode *node = queue[head++];
        if (node == NULL) {
            gap = true;
        } else {
            if (gap) return false;
            queue[tail++] = node->left;
            queue[tail++] = node->right;
        }
    }
    return true;
}

static int64_t seed = 958;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(void) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = 1 + next_random() % 1000;
    t->left = NULL;
    t->right = NULL;
    return t;
}

// Node i of the complete tree is a left child (side 0) when i is odd.
static int side_of(int i) { return (i + 1) % 2; }

static void set_child(TreeNode *parent, int side, TreeNode *child) {
    if (side == 0) parent->left = child;
    else parent->right = child;
}

static TreeNode *complete_tree(int n, TreeNode **nodes) {
    for (int i = 0; i < n; i++) nodes[i] = new_node();
    for (int i = 1; i < n; i++) set_child(nodes[(i - 1) / 2], side_of(i), nodes[i]);
    return nodes[0];
}

static TreeNode *random_tree(int n) {
    TreeNode *root = new_node();
    for (int i = 1; i < n; i++) {
        TreeNode *node = new_node();
        TreeNode *cur = root;
        for (;;) {
            if (next_random() % 2 == 0) {
                if (cur->left) cur = cur->left;
                else { cur->left = node; break; }
            } else {
                if (cur->right) cur = cur->right;
                else { cur->right = node; break; }
            }
        }
    }
    return root;
}

static TreeNode *make_tree(int kind, int n) {
    if (kind == 3) return random_tree(n);
    TreeNode *nodes[128];
    TreeNode *t = complete_tree(n, nodes);
    if (n < 2) return t;
    // nodes[] is the level order of the complete tree
    if (kind == 1) {
        TreeNode *last = nodes[n - 1];
        set_child(nodes[(n - 2) / 2], side_of(n - 1), NULL);
        TreeNode *parents[256];
        int sides[256], m = 0;
        for (int i = 0; i < n - 1; i++) {
            if (nodes[i]->left == NULL) { parents[m] = nodes[i]; sides[m++] = 0; }
            if (nodes[i]->right == NULL) { parents[m] = nodes[i]; sides[m++] = 1; }
        }
        int k = next_random() % m;
        set_child(parents[k], sides[k], last);
    } else if (kind == 2) {
        int leaves[128], m = 0;
        for (int i = 1; i < n; i++)
            if (nodes[i]->left == NULL && nodes[i]->right == NULL) leaves[m++] = i;
        int i = leaves[next_random() % m];
        set_child(nodes[(i - 1) / 2], side_of(i), NULL);
    } else if (kind == 4) {
        TreeNode *node = nodes[next_random() % n];
        TreeNode *l = node->left;
        node->left = node->right;
        node->right = l;
    }
    return t;
}

int main(void) {
    int rounds = 4000;
    TreeNode *trees[200];
    for (int i = 0; i < 200; i++) trees[i] = make_tree(i % 5, 100);
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 200; i++) {
            int64_t bit = is_complete_tree(trees[(r + i) % 200]) ? 1 : 0;
            total += bit;
            check = (check * 31 + bit + 1 + i) % 1000000007;
        }
    }
    printf("%d rounds over 200 trees of up to 100 nodes: %lld complete, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
