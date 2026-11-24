// LeetCode #1325 bench in C: the ★ arm (a recursive walk that settles both
// children first and deletes a leaf with the target's value) on the same 30
// trees of 3000 nodes and 300 passes, each linking every node back to its
// children first.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static TreeNode *remove_leaf_nodes(TreeNode *node, int target) {
    if (!node) return NULL;
    node->left = remove_leaf_nodes(node->left, target);
    node->right = remove_leaf_nodes(node->right, target);
    if (!node->left && !node->right && node->val == target) return NULL;
    return node;
}

static int64_t count(const TreeNode *node) {
    if (!node) return 0;
    return 1 + count(node->left) + count(node->right);
}

static int64_t seed = 1325;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define N 3000
#define TREES 30

typedef struct {
    TreeNode nodes[N];
    int64_t left[N];
    int64_t right[N];
} Tree;

static void build(Tree *t, int deep) {
    int64_t places[2 * N + 2][2];
    int64_t np = 2;
    places[0][0] = 0; places[0][1] = 1;
    places[1][0] = 0; places[1][1] = 0;
    for (int64_t i = 0; i < N; i++) {
        t->nodes[i].val = (int)(1 + next_random() % 3);
        t->left[i] = -1;
        t->right[i] = -1;
        if (i > 0) {
            int64_t r = next_random();
            int64_t at = deep && r % 4 != 0 ? np - 1 - next_random() % 2 : next_random() % np;
            int64_t parent = places[at][0], is_left = places[at][1];
            places[at][0] = places[np - 1][0];
            places[at][1] = places[np - 1][1];
            np--;
            if (is_left) t->left[parent] = i;
            else t->right[parent] = i;
            places[np][0] = i; places[np][1] = 1; np++;
            places[np][0] = i; places[np][1] = 0; np++;
        }
    }
}

int main(void) {
    Tree *trees = malloc(sizeof(Tree) * TREES);
    for (int t = 0; t < TREES; t++) build(&trees[t], t % 2 == 1);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 300; pass++) {
        for (int t = 0; t < TREES; t++) {
            Tree *tree = &trees[t];
            tree->nodes[check % N].val = (int)(1 + (check / 7) % 3);
            int target = (int)(1 + (check / 11) % 3);
            for (int64_t i = 0; i < N; i++) {
                tree->nodes[i].left = tree->left[i] >= 0 ? &tree->nodes[tree->left[i]] : NULL;
                tree->nodes[i].right = tree->right[i] >= 0 ? &tree->nodes[tree->right[i]] : NULL;
            }
            TreeNode *root = remove_leaf_nodes(&tree->nodes[0], target);
            int64_t top = root ? root->val : 0;
            check = (check * 31 + count(root) * 7 + top + pass) % 1000000007;
        }
    }
    printf("300 passes over 30 trees of 3000: checksum %lld\n", (long long)check);
    free(trees);
    return 0;
}
