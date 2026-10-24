// Benchmark: LeetCode #988 Smallest String Starting From Leaf -- the ★
// arm, a walk carrying the path, on random trees of 8500 nodes,
// LeetCode's largest. Mirrors smallest_from_leaf.kara, .rs, .py and
// go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct { char *items; int64_t len, cap; } Path;

static void walk(TreeNode *t, Path *path, char **best) {
    if (path->len == path->cap) {
        path->cap = path->cap ? path->cap * 2 : 16;
        path->items = realloc(path->items, (size_t)path->cap);
    }
    path->items[path->len++] = (char)(97 + t->val);
    if (t->left == NULL && t->right == NULL) {
        char *s = malloc((size_t)path->len + 1);
        for (int64_t i = 0; i < path->len; i++) s[i] = path->items[path->len - 1 - i];
        s[path->len] = 0;
        if (*best == NULL || strcmp(s, *best) < 0) {
            free(*best);
            *best = s;
        } else {
            free(s);
        }
    } else {
        if (t->left) walk(t->left, path, best);
        if (t->right) walk(t->right, path, best);
    }
    path->len--;
}

static char *smallest_from_leaf(TreeNode *root) {
    Path path = {0};
    char *best = NULL;
    walk(root, &path, &best);
    free(path.items);
    return best;
}

static int64_t seed = 988;

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
    TreeNode *root = new_node(next_random() % 4);
    for (int i = 1; i < n; i++) {
        TreeNode *node = new_node(next_random() % 4), *cur = root;
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
    int rounds = 100;
    TreeNode *trees[20];
    for (int i = 0; i < 20; i++) trees[i] = random_tree(8500);
    int64_t letters = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            char *s = smallest_from_leaf(trees[(r + i) % 20]);
            for (char *p = s; *p; p++) {
                letters++;
                check = (check * 31 + (unsigned char)*p) % 1000000007;
            }
            free(s);
        }
    }
    printf("%d rounds over 20 trees of 8500 nodes: %lld letters, checksum %lld\n", rounds,
           (long long)letters, (long long)check);
    return 0;
}
