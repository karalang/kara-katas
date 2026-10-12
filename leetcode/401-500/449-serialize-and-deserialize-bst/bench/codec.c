// Benchmark for #449: mirror of codec.kara (preorder, rebuilt with
// bounds) on 10 random search trees of 50,000 values, built once, then
// serialized and deserialized 20 times over.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

typedef struct {
    char *data;
    size_t len;
    size_t cap;
} Text;

static void text_reserve(Text *t, size_t extra) {
    if (t->len + extra > t->cap) {
        size_t cap = t->cap ? t->cap : 16;
        while (cap < t->len + extra) {
            cap *= 2;
        }
        t->data = realloc(t->data, cap);
        t->cap = cap;
    }
}

static TreeNode *new_node(int64_t val, TreeNode *left, TreeNode *right) {
    TreeNode *node = malloc(sizeof(TreeNode));
    node->val = val;
    node->left = left;
    node->right = right;
    return node;
}

static void free_tree(TreeNode *node) {
    if (node) {
        free_tree(node->left);
        free_tree(node->right);
        free(node);
    }
}

static void write_preorder(const TreeNode *node, Text *out) {
    if (node) {
        text_reserve(out, 24);
        if (out->len > 0) {
            out->data[out->len++] = ',';
        }
        out->len += (size_t)sprintf(out->data + out->len, "%lld", (long long)node->val);
        write_preorder(node->left, out);
        write_preorder(node->right, out);
    }
}

static Text serialize(const TreeNode *root) {
    Text out = {NULL, 0, 0};
    write_preorder(root, &out);
    return out;
}

// Builds the subtree of values from low to high, both inclusive, taking
// them from values[*at] onward.
static TreeNode *build(const int64_t *values, size_t count, size_t *at, int64_t low, int64_t high) {
    if (*at == count || values[*at] < low || values[*at] > high) {
        return NULL;
    }
    int64_t v = values[*at];
    *at += 1;
    TreeNode *left = build(values, count, at, low, v - 1);
    TreeNode *right = build(values, count, at, v + 1, high);
    return new_node(v, left, right);
}

static TreeNode *deserialize(const char *data, size_t len) {
    size_t cap = 16, count = 0;
    int64_t *values = malloc(cap * sizeof(int64_t));
    size_t i = 0;
    while (i < len) {
        int64_t sign = 1, x = 0;
        if (data[i] == '-') {
            sign = -1;
            i++;
        }
        while (i < len && data[i] != ',') {
            x = x * 10 + (data[i] - '0');
            i++;
        }
        if (count == cap) {
            cap *= 2;
            values = realloc(values, cap * sizeof(int64_t));
        }
        values[count++] = sign * x;
        i++;
    }
    size_t at = 0;
    TreeNode *root = build(values, count, &at, INT64_MIN, INT64_MAX);
    free(values);
    return root;
}

static TreeNode *insert(TreeNode *root, int64_t v) {
    TreeNode *fresh = new_node(v, NULL, NULL);
    if (!root) {
        return fresh;
    }
    TreeNode *node = root;
    for (;;) {
        if (v < node->val) {
            if (!node->left) {
                node->left = fresh;
                break;
            }
            node = node->left;
        } else {
            if (!node->right) {
                node->right = fresh;
                break;
            }
            node = node->right;
        }
    }
    return root;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { TREES = 10, N = 50000, ROUNDS = 20 };
    int64_t seed = 449;
    TreeNode *roots[TREES];
    int64_t *values = malloc(N * sizeof(int64_t));
    for (int64_t t = 0; t < TREES; t++) {
        // A shuffle of 0 to n - 1, spread out and shifted per tree.
        for (int64_t i = 0; i < N; i++) {
            values[i] = i * 3 + t;
        }
        for (int64_t i = 0; i < N; i++) {
            int64_t r = next_random(&seed) * 32768;
            r += next_random(&seed);
            int64_t j = i + r % (N - i);
            int64_t tmp = values[i];
            values[i] = values[j];
            values[j] = tmp;
        }
        TreeNode *root = NULL;
        for (int64_t i = 0; i < N; i++) {
            root = insert(root, values[i]);
        }
        roots[t] = root;
    }
    free(values);
    int64_t characters = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++) {
        for (int t = 0; t < TREES; t++) {
            Text text = serialize(roots[t]);
            TreeNode *back = deserialize(text.data, text.len);
            int64_t top = back ? back->val : -1;
            characters += (int64_t)text.len;
            checksum = (checksum * 31 + (int64_t)text.len + top) % 1000000007;
            free_tree(back);
            free(text.data);
        }
    }
    for (int t = 0; t < TREES; t++) {
        free_tree(roots[t]);
    }
    printf("%d rounds on %d trees of %d: %lld characters, checksum %lld\n", ROUNDS, TREES, N,
           (long long)characters, (long long)checksum);
    return 0;
}
