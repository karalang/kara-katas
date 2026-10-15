// Benchmark for #653: in order, then two ends, as the Kara ★ arm. The
// set of values already inserted is a byte per value.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof *v->data);
    }
    v->data[v->len++] = x;
}

static void in_order(TreeNode *node, Vec *values) {
    if (!node) return;
    in_order(node->left, values);
    push(values, node->val);
    in_order(node->right, values);
}

static int find_target(TreeNode *root, int64_t k) {
    Vec values = {0};
    in_order(root, &values);
    int found = 0;
    if (values.len >= 2) {
        int64_t low = 0, high = values.len - 1;
        while (low < high) {
            int64_t sum = values.data[low] + values.data[high];
            if (sum == k) { found = 1; break; }
            if (sum < k) low++;
            else high--;
        }
    }
    free(values.data);
    return found;
}

static int64_t seed = 653;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t size = 200000, queries = 300, count = 0;
    char *seen = calloc(1000000, 1);
    TreeNode *root = NULL;
    while (count < size) {
        int64_t hi = next_random();
        int64_t v = (hi * 32768 + next_random()) % 1000000;
        if (seen[v]) continue;
        seen[v] = 1;
        count++;
        TreeNode *c = malloc(sizeof *c);
        c->val = v;
        c->left = c->right = NULL;
        if (!root) { root = c; continue; }
        TreeNode *node = root;
        for (;;) {
            if (v < node->val) {
                if (node->left) node = node->left;
                else { node->left = c; break; }
            } else {
                if (node->right) node = node->right;
                else { node->right = c; break; }
            }
        }
    }
    int64_t found = 0, checksum = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t hi = next_random();
        int64_t k = (hi * 32768 + next_random()) % 3000000;
        int hit = find_target(root, k);
        found += hit;
        checksum = (checksum * 2 + hit) % 1000000007;
    }
    printf("%lld values, %lld targets: %lld found, checksum %lld\n", (long long)size,
           (long long)queries, (long long)found, (long long)checksum);
    return 0;
}
