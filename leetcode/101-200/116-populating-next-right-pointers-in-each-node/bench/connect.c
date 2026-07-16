/* LeetCode #116 — C mirror (raw *Node), O(1)-space next-pointer population.
 * Same algorithm and workload as connect.kara: each rep builds a depth-9 perfect tree (511 nodes)
 * over a data-dependent base, wires `next` with constant-space level-threading, folds a level hash.
 * K = 40000. The metal floor: manual malloc/free, raw pointer chase. */
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

typedef struct Node {
    long long val;
    struct Node *left, *right, *next;
} Node;

static Node *build_perfect(long long idx, long long max_idx, long long base) {
    if (idx > max_idx) return NULL;
    Node *n = (Node *)malloc(sizeof(Node));
    n->val = idx + base;
    n->next = NULL;
    n->left = build_perfect(2 * idx, max_idx, base);
    n->right = build_perfect(2 * idx + 1, max_idx, base);
    return n;
}

static void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

static void connect(Node *root) {
    Node *leftmost = root;
    while (leftmost != NULL && leftmost->left != NULL) {
        Node *head = leftmost;
        while (head != NULL) {
            head->left->next = head->right;
            if (head->next != NULL) head->right->next = head->next->left;
            head = head->next;
        }
        leftmost = leftmost->left;
    }
}

static long long level_hash(Node *root) {
    long long h = 1;
    Node *leftmost = root;
    while (leftmost != NULL) {
        Node *cur = leftmost;
        while (cur != NULL) {
            h = (h * 131 + cur->val + 1) % MOD;
            cur = cur->next;
        }
        h = (h * 31 + 7) % MOD;
        leftmost = leftmost->left;
    }
    return h;
}

int main(void) {
    const long long max_idx = 511; /* depth-9 perfect tree */
    long long acc = 0;
    for (long long rep = 0; rep < 40000; rep++) {
        long long base = acc % 100;
        Node *root = build_perfect(1, max_idx, base);
        connect(root);
        long long h = level_hash(root);
        acc = (acc * 131 + h) % MOD;
        free_tree(root);
    }
    printf("%lld\n", acc);
    return 0;
}
