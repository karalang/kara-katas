// LeetCode #2385: Amount of Time for Binary Tree to Be Infected -- the
// bench, the ★ arm in C: one post-order walk returning each subtree's
// height and the start's distance below it. The nodes are one malloc'd
// array linked by pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t height, distance;
} Part;

static Part walk(const TreeNode *node, int64_t start, int64_t *best) {
    if (!node) return (Part){0, -1};
    Part l = walk(node->left, start, best);
    Part r = walk(node->right, start, best);
    int64_t height = 1 + (l.height > r.height ? l.height : r.height);
    if (node->val == start) {
        int64_t own = l.height > r.height ? l.height : r.height;
        if (own > *best) *best = own;
        return (Part){height, 0};
    }
    if (l.distance >= 0) {
        if (l.distance + 1 + r.height > *best) *best = l.distance + 1 + r.height;
        return (Part){height, l.distance + 1};
    }
    if (r.distance >= 0) {
        if (r.distance + 1 + l.height > *best) *best = r.distance + 1 + l.height;
        return (Part){height, r.distance + 1};
    }
    return (Part){height, -1};
}

static int64_t amount_of_time(const TreeNode *root, int64_t start) {
    int64_t best = 0;
    walk(root, start, &best);
    return best;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2385;

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
    // 200 random trees of 1000 nodes, each asked from 400 starts, start s
    // of tree t being 1 + (37 s + t) % 1000
    int64_t check = 0;
    TreeNode *nodes = malloc(sizeof(TreeNode) * 1000);
    for (int64_t t = 0; t < 200; t++) {
        TreeNode *root = random_tree(nodes, 1000);
        for (int64_t s = 0; s < 400; s++) {
            check = (check * 31 + amount_of_time(root, 1 + (37 * s + t) % 1000)) % 1000000007;
        }
    }
    free(nodes);
    printf("200 trees of 1000, 400 starts each: checksum %lld\n", (long long)check);
    return 0;
}
