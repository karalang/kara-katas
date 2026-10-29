// LeetCode #1028: Recover a Tree From Preorder Traversal -- bench
// Mirrors ./recover_tree.kara; see ../README.md § Benchmarks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode *recover_from_preorder(const char *traversal, size_t len) {
    TreeNode **path = malloc(sizeof(TreeNode *) * (len + 1));
    size_t top = 0, i = 0;
    TreeNode *root = NULL;
    while (i < len) {
        size_t depth = 0;
        while (traversal[i] == '-') {
            depth++;
            i++;
        }
        int64_t value = 0;
        while (i < len && traversal[i] != '-') {
            value = value * 10 + (traversal[i] - '0');
            i++;
        }
        TreeNode *node = malloc(sizeof(TreeNode));
        node->val = value;
        node->left = node->right = NULL;
        if (top > depth) top = depth;
        if (top > 0) {
            TreeNode *parent = path[top - 1];
            if (parent->left == NULL) parent->left = node;
            else parent->right = node;
        } else {
            root = node;
        }
        path[top++] = node;
    }
    free(path);
    return root;
}

static void free_tree(TreeNode *node) {
    if (!node) return;
    free_tree(node->left);
    free_tree(node->right);
    free(node);
}

// a fold of the tree's values and shape
static int64_t digest(const TreeNode *node) {
    if (!node) return 1;
    return (node->val + 3 * digest(node->left) + 7 * digest(node->right)) % 1000000007;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random_value(int64_t *seed, int64_t top) {
    int64_t a = next_random(seed);
    int64_t b = next_random(seed);
    return (a * 32768 + b) % top + 1;
}

typedef struct {
    char *data;
    size_t len, cap;
} Buf;

static void put(Buf *b, const char *s, size_t n) {
    if (b->len + n + 1 > b->cap) {
        while (b->len + n + 1 > b->cap) b->cap = b->cap ? b->cap * 2 : 64;
        b->data = realloc(b->data, b->cap);
    }
    memcpy(b->data + b->len, s, n);
    b->len += n;
    b->data[b->len] = 0;
}

static void write_tree(int64_t at, int64_t depth, const int64_t *vals, const int64_t *left,
                       const int64_t *right, Buf *out) {
    for (int64_t d = 0; d < depth; d++) put(out, "-", 1);
    char num[24];
    int n = snprintf(num, sizeof num, "%lld", (long long)vals[at]);
    put(out, num, (size_t)n);
    if (left[at] >= 0) write_tree(left[at], depth + 1, vals, left, right, out);
    if (right[at] >= 0) write_tree(right[at], depth + 1, vals, left, right, out);
}

static Buf make_traversal(int64_t *seed, int64_t n) {
    int64_t *vals = malloc(sizeof(int64_t) * n);
    int64_t *left = malloc(sizeof(int64_t) * n);
    int64_t *right = malloc(sizeof(int64_t) * n);
    for (int64_t k = 0; k < n; k++) {
        int64_t v = random_value(seed, 1000000000);
        vals[k] = v;
        left[k] = right[k] = -1;
        int64_t at = 0;
        while (k > 0) {
            if (v < vals[at]) {
                if (left[at] < 0) {
                    left[at] = k;
                    break;
                }
                at = left[at];
            } else {
                if (right[at] < 0) {
                    right[at] = k;
                    break;
                }
                at = right[at];
            }
        }
    }
    Buf out = {0};
    write_tree(0, 0, vals, left, right, &out);
    free(vals);
    free(left);
    free(right);
    return out;
}

int main(void) {
    const int count = 200, rounds = 50;
    int64_t seed = 1028;
    Buf traversals[200];
    int64_t letters = 0;
    for (int k = 0; k < count; k++) {
        traversals[k] = make_traversal(&seed, 1000);
        letters += (int64_t)traversals[k].len;
    }
    int64_t check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            TreeNode *root = recover_from_preorder(traversals[k].data, traversals[k].len);
            check = (check * 131 + digest(root)) % 1000000007;
            free_tree(root);
        }
    }
    printf("%d traversals of 1000 nodes, %lld letters, %d rounds: checksum %lld\n", count,
           (long long)letters, rounds, (long long)check);
    for (int k = 0; k < count; k++) free(traversals[k].data);
    return 0;
}
