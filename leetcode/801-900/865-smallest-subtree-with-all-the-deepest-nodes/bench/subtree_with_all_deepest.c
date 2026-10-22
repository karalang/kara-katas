// LeetCode #865: Smallest Subtree with all the Deepest Nodes -- C mirror
// of the bench program (the ★ arm, one recursive pass).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

#define MAXV 501

// the depth of the subtree under `node`, and in `*found` the root of the
// smallest subtree holding all its deepest nodes
static int64_t deepest(Node *node, Node **found) {
    if (!node) {
        *found = NULL;
        return 0;
    }
    Node *l, *r;
    int64_t dl = deepest(node->left, &l);
    int64_t dr = deepest(node->right, &r);
    if (dl == dr) {
        *found = node;
        return dl + 1;
    }
    if (dl > dr) {
        *found = l;
        return dl + 1;
    }
    *found = r;
    return dr + 1;
}

static Node *subtree_with_all_deepest(Node *root) {
    Node *found;
    deepest(root, &found);
    return found;
}

static int64_t seed = 865;

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
    int64_t n = 500, rounds = 300000;
    Node *created[MAXV];
    Node *root = random_tree(n, created);
    Node *nodes[MAXV];
    Node *stack[MAXV];
    int64_t sp = 0, count = 0;
    stack[sp++] = root;
    while (sp > 0) {
        Node *node = stack[--sp];
        if (node->left) {
            stack[sp++] = node->left;
        }
        if (node->right) {
            stack[sp++] = node->right;
        }
        nodes[count++] = node;
    }
    Node leaf = {n, NULL, NULL};
    int64_t total = 0, check = 0;
    for (int64_t q = 0; q < rounds; q++) {
        Node *at = nodes[next_random() % n];
        while (at->left && at->right) {
            at = nodes[next_random() % n];
        }
        int on_left = at->left == NULL;
        if (on_left) {
            at->left = &leaf;
        } else {
            at->right = &leaf;
        }
        Node *f = subtree_with_all_deepest(root);
        int64_t found = f ? f->val : -1;
        if (on_left) {
            at->left = NULL;
        } else {
            at->right = NULL;
        }
        total += found;
        check = (check * 31 + found + 1) % 1000000007;
    }
    printf("%lld rounds on %lld nodes: answers sum to %lld, checksum %lld\n", (long long)rounds, (long long)n,
           (long long)total, (long long)check);
    for (int64_t k = 0; k < n; k++) {
        free(created[k]);
    }
    return 0;
}
