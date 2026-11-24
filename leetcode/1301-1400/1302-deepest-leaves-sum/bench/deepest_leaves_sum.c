// LeetCode #1302 bench in C: the ★ arm (a breadth-first walk a level at a
// time, the queue an array of n pointers read from a moving head, since each
// node is queued once) on the same 50 trees of 10^4 nodes and 50 passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int deepest_leaves_sum(TreeNode *root, int n) {
    TreeNode **queue = malloc(sizeof(TreeNode *) * (size_t)n);
    size_t head = 0, tail = 0;
    if (root) queue[tail++] = root;
    int sum = 0;
    while (tail > head) {
        sum = 0;
        size_t end = tail;
        while (head < end) {
            TreeNode *node = queue[head++];
            sum += node->val;
            if (node->left) queue[tail++] = node->left;
            if (node->right) queue[tail++] = node->right;
        }
    }
    free(queue);
    return sum;
}

static int64_t seed = 1302;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(void) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = (int)(1 + next_random() % 100);
    t->left = NULL;
    t->right = NULL;
    return t;
}

typedef struct {
    TreeNode *node;
    int left;
} Place;

static void build(int n, int level_order, TreeNode **nodes) {
    TreeNode *root = new_node();
    int count = 0;
    nodes[count++] = root;
    if (level_order) {
        TreeNode **level = malloc(sizeof(TreeNode *) * (size_t)(n + 1));
        size_t head = 0, tail = 0;
        level[tail++] = root;
        while (count < n) {
            TreeNode *at = level[head++];
            for (int side = 0; side < 2; side++) {
                if (count < n && next_random() % 4 != 0) {
                    TreeNode *node = new_node();
                    if (side == 0) at->left = node; else at->right = node;
                    level[tail++] = node;
                    nodes[count++] = node;
                }
            }
            if (tail == head) {
                head = 0;
                tail = 0;
                level[tail++] = at;
            }
        }
        free(level);
    } else {
        Place *places = malloc(sizeof(Place) * (size_t)(n + 2));
        size_t len = 0;
        places[len++] = (Place){root, 1};
        places[len++] = (Place){root, 0};
        while (count < n) {
            size_t k = (size_t)(next_random() % (int64_t)len);
            Place p = places[k];
            places[k] = places[--len];
            TreeNode *node = new_node();
            if (p.left) p.node->left = node; else p.node->right = node;
            places[len++] = (Place){node, 1};
            places[len++] = (Place){node, 0};
            nodes[count++] = node;
        }
        free(places);
    }
}

int main(void) {
    int n = 10000;
    TreeNode **trees[50];
    for (int t = 0; t < 50; t++) {
        trees[t] = malloc(sizeof(TreeNode *) * (size_t)n);
        build(n, t % 2 == 1, trees[t]);
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 50; pass++) {
        for (int t = 0; t < 50; t++) {
            TreeNode **nodes = trees[t];
            nodes[check % n]->val = (int)(1 + (check / 7) % 100);
            int sum = deepest_leaves_sum(nodes[0], n);
            check = (check * 31 + sum + pass) % 1000000007;
        }
    }
    printf("50 passes over 50 trees of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
