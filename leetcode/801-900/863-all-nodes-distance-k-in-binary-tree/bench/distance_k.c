// LeetCode #863: All Nodes Distance K in Binary Tree -- C mirror of the
// bench program (the ★ arm, parents, then a breadth-first search). C has
// no hash map, so the parents and the reached set are arrays indexed by
// value, which the unique values from 0 to 500 allow.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

#define MAXV 501

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// writes the answer to `found` and returns its length
static int64_t distance_k(Node *root, int64_t target, int64_t k, int64_t *found) {
    Node *parent[MAXV] = {0};
    char seen[MAXV] = {0};
    Node *stack[MAXV];
    Node *level[MAXV], *next[MAXV];
    int64_t sp = 0;
    Node *start = NULL;
    if (root) {
        stack[sp++] = root;
    }
    while (sp > 0) {
        Node *node = stack[--sp];
        if (node->val == target) {
            start = node;
        }
        if (node->left) {
            parent[node->left->val] = node;
            stack[sp++] = node->left;
        }
        if (node->right) {
            parent[node->right->val] = node;
            stack[sp++] = node->right;
        }
    }
    if (!start) {
        return 0;
    }
    seen[start->val] = 1;
    int64_t len = 0;
    level[len++] = start;
    for (int64_t step = 0; step < k; step++) {
        int64_t nlen = 0;
        for (int64_t i = 0; i < len; i++) {
            Node *node = level[i];
            Node *near[3] = {node->left, node->right, parent[node->val]};
            for (int t = 0; t < 3; t++) {
                Node *m = near[t];
                if (m && !seen[m->val]) {
                    seen[m->val] = 1;
                    next[nlen++] = m;
                }
            }
        }
        for (int64_t i = 0; i < nlen; i++) {
            level[i] = next[i];
        }
        len = nlen;
    }
    for (int64_t i = 0; i < len; i++) {
        found[i] = level[i]->val;
    }
    qsort(found, len, sizeof(int64_t), cmp);
    return len;
}

static int64_t seed = 863;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static Node *random_tree(int64_t n, Node **nodes) {
    int64_t vals[MAXV];
    for (int64_t v = 0; v < n; v++) {
        vals[v] = v;
    }
    for (int64_t i = 1; i < n; i++) {
        int64_t j = next_random() % (i + 1);
        int64_t t = vals[i];
        vals[i] = vals[j];
        vals[j] = t;
    }
    for (int64_t k = 0; k < n; k++) {
        Node *node = malloc(sizeof(Node));
        node->val = vals[k];
        node->left = node->right = NULL;
        if (k > 0) {
            for (;;) {
                Node *parent = nodes[next_random() % k];
                if (next_random() % 2 == 0) {
                    if (!parent->left) {
                        parent->left = node;
                        break;
                    }
                } else if (!parent->right) {
                    parent->right = node;
                    break;
                }
            }
        }
        nodes[k] = node;
    }
    return n ? nodes[0] : NULL;
}

int main(void) {
    int64_t n = 500;
    int64_t queries = 200000;
    Node *nodes[MAXV];
    Node *root = random_tree(n, nodes);
    int64_t found[MAXV];
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t target = next_random() % n;
        int64_t k = next_random() % 20;
        int64_t len = distance_k(root, target, k, found);
        total += len;
        for (int64_t i = 0; i < len; i++) {
            check = (check * 31 + found[i] + 1) % 1000000007;
        }
    }
    printf("%lld queries on %lld nodes: %lld nodes found, checksum %lld\n", (long long)queries, (long long)n,
           (long long)total, (long long)check);
    for (int64_t k = 0; k < n; k++) {
        free(nodes[k]);
    }
    return 0;
}
