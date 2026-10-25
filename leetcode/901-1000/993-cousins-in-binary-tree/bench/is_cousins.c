// Benchmark: LeetCode #993 Cousins in Binary Tree -- the ★ arm, a
// breadth-first search a level at a time, on random trees of 100 nodes,
// LeetCode's largest. Mirrors is_cousins.kara, .rs, .py and go-seq/.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct { TreeNode *node; int64_t parent; } Entry;

typedef struct { Entry *items; int64_t len, cap; } Level;

static void push(Level *l, Entry e) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, sizeof(Entry) * (size_t)l->cap);
    }
    l->items[l->len++] = e;
}

static bool is_cousins(TreeNode *root, int64_t x, int64_t y) {
    Level level = {0};
    push(&level, (Entry){root, -1});
    while (level.len > 0) {
        int64_t px = -1, py = -1;
        Level next = {0};
        for (int64_t i = 0; i < level.len; i++) {
            TreeNode *node = level.items[i].node;
            if (node->val == x) px = level.items[i].parent;
            if (node->val == y) py = level.items[i].parent;
            if (node->left) push(&next, (Entry){node->left, node->val});
            if (node->right) push(&next, (Entry){node->right, node->val});
        }
        free(level.items);
        if (px >= 0 && py >= 0) {
            free(next.items);
            return px != py;
        }
        if (px >= 0 || py >= 0) {
            free(next.items);
            return false;
        }
        level = next;
    }
    free(level.items);
    return false;
}

static int64_t seed = 993;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(int64_t val) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = val;
    t->left = NULL;
    t->right = NULL;
    return t;
}

static TreeNode *random_tree(int n) {
    int64_t vals[100];
    for (int i = 0; i < n; i++) vals[i] = i + 1;
    for (int i = n - 1; i > 0; i--) {
        int64_t j = next_random() % (i + 1);
        int64_t t = vals[i];
        vals[i] = vals[j];
        vals[j] = t;
    }
    TreeNode *root = new_node(vals[0]);
    for (int k = 1; k < n; k++) {
        TreeNode *node = new_node(vals[k]), *cur = root;
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
    int rounds = 500;
    TreeNode *trees[20];
    for (int i = 0; i < 20; i++) trees[i] = random_tree(100);
    int64_t found = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int t = 0; t < 20; t++) {
            int64_t d = 1 + (r * 7 + t) % 99;
            for (int64_t x = 1; x <= 100; x++) {
                int64_t y = 1 + (x - 1 + d) % 100;
                bool got = is_cousins(trees[(r + t) % 20], x, y);
                if (got) found++;
                check = (check * 31 + (got ? 2 : 1)) % 1000000007;
            }
        }
    }
    printf("%d rounds over 20 trees of 100 nodes: %lld cousin pairs, checksum %lld\n", rounds,
           (long long)found, (long long)check);
    return 0;
}
