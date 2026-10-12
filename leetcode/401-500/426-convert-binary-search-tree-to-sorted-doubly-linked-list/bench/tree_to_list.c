// Benchmark for #426: mirror of tree_to_list.kara (the in-order
// recursion). Nodes are malloc'd; the walk frees each node as it passes,
// where the Kāra program breaks its links and the count drops to zero.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int64_t val; struct Node *left, *right; } Node;

static void link(Node *node, Node **first, Node **last) {
    if (!node) return;
    link(node->left, first, last);
    if (*last) {
        (*last)->right = node;
        node->left = *last;
    } else {
        *first = node;
    }
    *last = node;
    link(node->right, first, last);
}

static Node *tree_to_doubly_list(Node *root) {
    Node *first = NULL, *last = NULL;
    link(root, &first, &last);
    if (!first) return NULL;
    first->left = last;
    last->right = first;
    return first;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static Node *insert(Node *root, int64_t val) {
    if (!root) {
        Node *n = malloc(sizeof *n);
        n->val = val;
        n->left = n->right = NULL;
        return n;
    }
    if (val < root->val) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}

int main(int argc, char **argv) {
    int64_t n = 50000;
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 20;
    int64_t seed = 426;
    int64_t *order = malloc(n * sizeof *order);
    for (int64_t v = 0; v < n; v++) order[v] = v;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < n - 1; i++) {
            int64_t a = step(&seed);
            int64_t b = step(&seed);
            int64_t j = i + (a * 32768 + b) % (n - i);
            int64_t keep = order[i];
            order[i] = order[j];
            order[j] = keep;
        }
        Node *root = NULL;
        for (int64_t i = 0; i < n; i++) root = insert(root, order[i]);
        Node *head = tree_to_doubly_list(root);
        checksum = (checksum * 31 + head->left->val) % 1000000007;
        Node *cur = head;
        for (int64_t i = 0; i < n; i++) {
            checksum = (checksum * 31 + cur->val) % 1000000007;
            Node *next = cur->right;
            free(cur);
            cur = next;
        }
    }
    printf("%lld rounds on %lld nodes: checksum %lld\n", (long long)rounds, (long long)n, (long long)checksum);
    free(order);
    return 0;
}
