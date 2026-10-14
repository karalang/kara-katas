// Benchmark for #549: C mirror of the ★ arm (post-order, two lengths a
// node); see binary_tree_longest_consecutive_sequence_ii.kara. Plain
// pointers, the nodes from one array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

typedef struct {
    int64_t rise, fall;
} Runs;

static Runs walk(const Node *node, int64_t *best) {
    int64_t rise = 1, fall = 1;
    if (node->left) {
        const Node *l = node->left;
        Runs a = walk(l, best);
        if (l->val == node->val + 1) rise = a.rise + 1;
        else if (l->val == node->val - 1) fall = a.fall + 1;
    }
    if (node->right) {
        const Node *r = node->right;
        Runs b = walk(r, best);
        if (r->val == node->val + 1) { if (b.rise + 1 > rise) rise = b.rise + 1; }
        else if (r->val == node->val - 1) { if (b.fall + 1 > fall) fall = b.fall + 1; }
    }
    if (rise + fall - 1 > *best) *best = rise + fall - 1;
    return (Runs){rise, fall};
}

static int64_t longest_consecutive(const Node *root) {
    int64_t best = 0;
    if (root) walk(root, &best);
    return best;
}

static int64_t seed = 549;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int count = 20, size = 30000;
    Node *pool = calloc((size_t)count * size, sizeof(Node));
    Node *firsts[20][16];
    for (int g = 0; g < count; g++) {
        int64_t spread = 3 + g % 4;
        Node *nodes = pool + (size_t)g * size;
        nodes[0].val = next_random() % spread;
        firsts[g][0] = &nodes[0];
        for (int t = 1; t < size; t++) {
            Node *c = &nodes[t];
            c->val = next_random() % spread;
            Node *node = &nodes[0];
            for (;;) {
                if (next_random() % 2 == 0) {
                    if (node->left) node = node->left;
                    else { node->left = c; break; }
                } else {
                    if (node->right) node = node->right;
                    else { node->right = c; break; }
                }
            }
            if (t < 16) firsts[g][t] = c;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < 60; round++)
        for (int g = 0; g < count; g++) {
            int64_t d = longest_consecutive(firsts[g][(round * 7 + g) % 16]);
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    printf("%d trees, 60 rounds each: lengths %lld, checksum %lld\n", count, (long long)total,
           (long long)checksum);
    free(pool);
    return 0;
}
