// LeetCode #897 bench: the ★ arm (an in-order walk that relinks as it
// goes) on 200,000 search trees of 100 nodes, LeetCode's largest, each
// made by putting in 100 random values from 0 to 1000; each chain is
// walked into a checksum. The same algorithm as increasing_bst.kara.
// Each tree's nodes are freed once its chain has been walked.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

static Node *new_node(int64_t val) {
    Node *n = malloc(sizeof(Node));
    n->val = val;
    n->left = NULL;
    n->right = NULL;
    return n;
}

static void relink(Node *node, Node **tail) {
    if (node) {
        relink(node->left, tail);
        node->left = NULL;
        (*tail)->right = node;
        *tail = node;
        relink(node->right, tail);
    }
}

static Node *increasing_bst(Node *root) {
    Node head = {-1, NULL, NULL};
    Node *tail = &head;
    relink(root, &tail);
    return head.right;
}

static int64_t seed = 897;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t nodes = 0, check = 0;
    for (int t = 0; t < 200000; t++) {
        Node *root = new_node(next_random() % 1001);
        for (int k = 1; k < 100; k++) {
            int64_t v = next_random() % 1001;
            Node *cur = root;
            for (;;) {
                if (v < cur->val) {
                    if (cur->left) cur = cur->left;
                    else { cur->left = new_node(v); break; }
                } else {
                    if (cur->right) cur = cur->right;
                    else { cur->right = new_node(v); break; }
                }
            }
        }
        Node *cur = increasing_bst(root);
        while (cur) {
            nodes++;
            check = (check * 31 + cur->val) % 1000000007;
            Node *next = cur->right;
            free(cur);
            cur = next;
        }
    }
    printf("200000 trees of 100 nodes: %lld in the chains, checksum %lld\n", (long long)nodes, (long long)check);
    return 0;
}
