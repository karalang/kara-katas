// Benchmark: LeetCode #968 Binary Tree Cameras -- the ★ arm, greedy from
// the leaves, on random trees of 1000 nodes, LeetCode's largest. Mirrors
// min_camera_cover.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

// 0 not yet covered, 1 holds a camera, 2 covered without one.
static int watch(TreeNode *t, int64_t *cameras) {
    if (t == NULL) return 2;
    int l = watch(t->left, cameras);
    int r = watch(t->right, cameras);
    if (l == 0 || r == 0) {
        (*cameras)++;
        return 1;
    }
    if (l == 1 || r == 1) return 2;
    return 0;
}

static int64_t min_camera_cover(TreeNode *root) {
    int64_t cameras = 0;
    if (watch(root, &cameras) == 0) cameras++;
    return cameras;
}

static int64_t seed = 968;

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
    TreeNode *root = new_node();
    for (int i = 1; i < n; i++) {
        TreeNode *node = new_node(), *cur = root;
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

int main(void) {
    int rounds = 200;
    TreeNode *trees[200];
    for (int i = 0; i < 200; i++) trees[i] = random_tree(1000);
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 200; i++) {
            int64_t c = min_camera_cover(trees[(r + i) % 200]);
            total += c;
            check = (check * 31 + c + i) % 1000000007;
        }
    }
    printf("%d rounds over 200 trees of 1000 nodes: %lld cameras, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
