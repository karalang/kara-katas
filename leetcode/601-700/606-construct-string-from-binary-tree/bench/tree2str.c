// Benchmark for #606: C mirror of the ★ arm (write it out); see
// tree2str.kara. The nodes are malloc'd one at a time and never freed,
// as the trees live to the end; the string is a `malloc`'d buffer that
// doubles when full, and each value is formatted into a small buffer
// on the stack before it is appended.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    char *data;
    size_t len, cap;
} Buffer;

static void append(Buffer *b, const char *s, size_t n) {
    if (b->len + n > b->cap) {
        while (b->len + n > b->cap) b->cap = b->cap ? b->cap * 2 : 16;
        b->data = realloc(b->data, b->cap);
    }
    memcpy(b->data + b->len, s, n);
    b->len += n;
}

static void write_node(const TreeNode *node, Buffer *out) {
    char digits[24];
    int n = snprintf(digits, sizeof digits, "%lld", (long long)node->val);
    append(out, digits, (size_t)n);
    if (node->left || node->right) {
        append(out, "(", 1);
        if (node->left) write_node(node->left, out);
        append(out, ")", 1);
    }
    if (node->right) {
        append(out, "(", 1);
        write_node(node->right, out);
        append(out, ")", 1);
    }
}

static Buffer tree2str(const TreeNode *root) {
    Buffer out = {NULL, 0, 0};
    if (root) write_node(root, &out);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *new_node(int64_t v) {
    TreeNode *n = malloc(sizeof *n);
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

int main(void) {
    enum { TREES = 20, ROUNDS = 200, SIZE = 10000 };
    int64_t seed = 606;
    static TreeNode *all[TREES][SIZE];
    for (int g = 0; g < TREES; g++) {
        int64_t lean = 50 + 2 * g;
        TreeNode *root = new_node(next_random(&seed) % 2001 - 1000);
        all[g][0] = root;
        for (int i = 1; i < SIZE; i++) {
            TreeNode *c = new_node(next_random(&seed) % 2001 - 1000);
            TreeNode *node = root;
            for (;;) {
                if (next_random(&seed) % 100 < lean) {
                    if (node->left) node = node->left;
                    else { node->left = c; break; }
                } else {
                    if (node->right) node = node->right;
                    else { node->right = c; break; }
                }
            }
            all[g][i] = c;
        }
    }
    int64_t length = 0, checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++)
        for (int64_t t = 0; t < TREES; t++) {
            int64_t k = (r * 37 + t * 11) % 16;
            Buffer s = tree2str(all[t][k]);
            length += (int64_t)s.len;
            for (size_t i = 0; i < s.len; i++)
                if (i % 101 == 0) checksum = (checksum * 31 + s.data[i]) % 1000000007;
            free(s.data);
        }
    printf("%d trees, %d times each: %lld characters, checksum %lld\n", TREES, ROUNDS, (long long)length,
           (long long)checksum);
    return 0;
}
