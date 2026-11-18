// LeetCode #2265: Count Nodes Equal to Average of Subtree -- C mirror of
// the ★ arm (average.kara): the same random trees, the nodes in one
// malloc'd array linked by pointers, each counted by one post-order walk
// returning the sum and the size. Output is byte-identical to
// average.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t sum, size;
} Part;

static Part sum_and_size(const TreeNode *node, int64_t *matches) {
    if (!node) return (Part){0, 0};
    Part l = sum_and_size(node->left, matches);
    Part r = sum_and_size(node->right, matches);
    Part p = {l.sum + r.sum + node->val, l.size + r.size + 1};
    if (p.sum / p.size == node->val) (*matches)++;
    return p;
}

static int64_t average_of_subtree(const TreeNode *root) {
    int64_t matches = 0;
    sum_and_size(root, &matches);
    return matches;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2265;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *random_tree(TreeNode *nodes, int n, int64_t top) {
    for (int i = 0; i < n; i++) {
        nodes[i].val = (int32_t)(next_random() % (top + 1));
        nodes[i].left = nodes[i].right = NULL;
    }
    for (int k = 1; k < n; k++) {
        TreeNode *at = &nodes[next_random() % k];
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
    int64_t check = 0;
    TreeNode *nodes = malloc(sizeof(TreeNode) * 1000);
    for (int t = 0; t < 500; t++) {
        TreeNode *root = random_tree(nodes, 1000, 1000);
        for (int r = 0; r < 20; r++) check = (check * 31 + average_of_subtree(root)) % 1000000007;
    }
    free(nodes);
    printf("500 trees of 1000, 20 times: checksum %lld\n", (long long)check);
    return 0;
}
