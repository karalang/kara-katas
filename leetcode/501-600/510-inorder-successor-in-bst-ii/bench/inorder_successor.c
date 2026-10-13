// Benchmark for #510: C mirror of the ★ arm (down the right subtree, or
// up to the first larger ancestor); see inorder_successor.kara. The
// parent link is a plain pointer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right, *parent;
} Node;

static Node *inorder_successor(Node *node) {
    if (node->right) {
        Node *cur = node->right;
        while (cur->left) cur = cur->left;
        return cur;
    }
    for (Node *up = node->parent; up; up = up->parent) {
        if (up->val > node->val) return up;
    }
    return NULL;
}

// ---- benchmark --------------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static Node *new_node(int64_t v) {
    Node *n = malloc(sizeof(Node));
    n->val = v;
    n->left = n->right = n->parent = NULL;
    return n;
}

// Every node of the search tree of the values, in insertion order.
static Node **build(const int64_t *values, int64_t size) {
    Node **nodes = malloc(size * sizeof(Node *));
    Node *root = new_node(values[0]);
    nodes[0] = root;
    for (int64_t i = 1; i < size; i++) {
        int64_t v = values[i];
        Node *leaf = new_node(v);
        Node *node = root;
        for (;;) {
            Node **slot = v < node->val ? &node->left : &node->right;
            if (*slot) {
                node = *slot;
            } else {
                leaf->parent = node;
                *slot = leaf;
                break;
            }
        }
        nodes[i] = leaf;
    }
    return nodes;
}

int main(void) {
    // 100 random search trees of 10,000 different values, the j-th value
    // j * 20 plus less than 20, shuffled, built once. Then the successor
    // of every node, 50 times over.
    int64_t trees = 100, size = 10000;
    int64_t seed = 510;
    Node ***all = malloc(trees * sizeof(Node **));
    int64_t *values = malloc(size * sizeof(int64_t));
    for (int64_t t = 0; t < trees; t++) {
        for (int64_t j = 0; j < size; j++) values[j] = j * 20 + next_random(&seed) % 20 - 100000;
        for (int64_t i = 1; i < size; i++) {
            int64_t k = next_random(&seed) % (i + 1);
            int64_t x = values[i];
            values[i] = values[k];
            values[k] = x;
        }
        all[t] = build(values, size);
    }
    int64_t nulls = 0, checksum = 0;
    for (int r = 0; r < 50; r++) {
        for (int64_t t = 0; t < trees; t++) {
            for (int64_t i = 0; i < size; i++) {
                Node *s = inorder_successor(all[t][i]);
                if (s) checksum = (checksum + s->val + 100000) % 1000000007;
                else nulls++;
            }
        }
    }
    printf("%lld trees of %lld nodes, 50 times each: %lld without a successor, checksum %lld\n",
           (long long)trees, (long long)size, (long long)nulls, (long long)checksum);
    return 0;
}
