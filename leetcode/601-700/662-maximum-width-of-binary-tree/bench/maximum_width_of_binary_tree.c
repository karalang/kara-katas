// Benchmark for #662: level by level, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

typedef struct {
    TreeNode *node;
    int64_t place;
} Item;

static int64_t width_of_binary_tree(TreeNode *root) {
    int64_t best = 0;
    size_t n = 0;
    Item *level = malloc(sizeof(Item));
    if (root) {
        level[n++] = (Item){root, 0};
    }
    while (n > 0) {
        int64_t first = level[0].place;
        int64_t last = level[n - 1].place;
        if (last - first + 1 > best) {
            best = last - first + 1;
        }
        size_t m = 0, ncap = 1;
        Item *next = malloc(sizeof(Item));
        for (size_t i = 0; i < n; i++) {
            int64_t p = (level[i].place - first) * 2;
            TreeNode *kids[2] = {level[i].node->left, level[i].node->right};
            for (int k = 0; k < 2; k++) {
                if (kids[k]) {
                    if (m == ncap) {
                        ncap *= 2;
                        next = realloc(next, ncap * sizeof(Item));
                    }
                    next[m++] = (Item){kids[k], p + k};
                }
            }
        }
        free(level);
        level = next;
        n = m;
    }
    free(level);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *leaf(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = NULL;
    n->right = NULL;
    return n;
}

static TreeNode *grown_tree(int64_t count, int64_t levels, int64_t *seed) {
    TreeNode *root = leaf(next_random(seed) % 201 - 100);
    int64_t made = 1;
    while (made < count) {
        TreeNode *at = root;
        int64_t depth = 1;
        int placed = 0;
        while (!placed && depth < levels) {
            if (next_random(seed) % 2 == 0) {
                if (at->left) {
                    at = at->left;
                } else {
                    at->left = leaf(next_random(seed) % 201 - 100);
                    placed = 1;
                }
            } else {
                if (at->right) {
                    at = at->right;
                } else {
                    at->right = leaf(next_random(seed) % 201 - 100);
                    placed = 1;
                }
            }
            depth++;
        }
        if (placed) {
            made++;
        }
    }
    return root;
}

static void free_tree(TreeNode *n) {
    if (n) {
        free_tree(n->left);
        free_tree(n->right);
        free(n);
    }
}

int main(void) {
    int64_t seed = 662;
    TreeNode *trees[8];
    for (int i = 0; i < 8; i++) {
        trees[i] = grown_tree(3000, 31, &seed);
    }
    int64_t rounds = 20000;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t w = width_of_binary_tree(trees[r % 8]);
        sum = (sum * 31 + w + r) % 1000000007;
    }
    printf("8 trees of 3000 nodes, %lld rounds: checksum %lld\n", (long long)rounds, (long long)sum);
    for (int i = 0; i < 8; i++) {
        free_tree(trees[i]);
    }
    return 0;
}
