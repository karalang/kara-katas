/* LeetCode #117 — C mirror (raw *Node), O(1)-space next-pointer population on an arbitrary tree.
 * Same algorithm and workload as connect.kara: each rep builds a ~500-node pseudo-random BST (fixed
 * shape, data-dependent value base), wires `next` with the dummy-head + tail threading, folds a
 * level hash. K = 16000. The metal floor: manual malloc/free, raw pointer chase. */
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

typedef struct Node {
    long long val;
    struct Node *left, *right, *next;
} Node;

static Node *new_node(long long v) {
    Node *n = (Node *)malloc(sizeof(Node));
    n->val = v;
    n->left = n->right = n->next = NULL;
    return n;
}

static Node *insert(Node *root, long long v) {
    if (root == NULL) return new_node(v);
    if (v < root->val) root->left = insert(root->left, v);
    else root->right = insert(root->right, v);
    return root;
}

static Node *build_bst(long long count, long long base) {
    Node *root = NULL;
    long long s = 88172645LL;
    for (long long i = 0; i < count; i++) {
        s = (s * 1103515245LL + 12345LL) % 2147483648LL;
        root = insert(root, (s % 100000LL) + base);
    }
    return root;
}

static void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

static void connect(Node *root) {
    Node *leftmost = root;
    while (leftmost != NULL) {
        Node dummy;
        dummy.next = NULL;
        Node *tail = &dummy;
        Node *cur = leftmost;
        while (cur != NULL) {
            if (cur->left != NULL) {
                tail->next = cur->left;
                tail = cur->left;
            }
            if (cur->right != NULL) {
                tail->next = cur->right;
                tail = cur->right;
            }
            cur = cur->next;
        }
        leftmost = dummy.next;
    }
}

static long long level_hash(Node *root) {
    long long h = 1;
    Node *head = root;
    while (head != NULL) {
        Node *cur = head;
        while (cur != NULL) {
            h = (h * 131 + cur->val + 1) % MOD;
            cur = cur->next;
        }
        h = (h * 31 + 7) % MOD;
        Node *nh = NULL;
        Node *scan = head;
        while (scan != NULL) {
            if (scan->left != NULL) { nh = scan->left; break; }
            if (scan->right != NULL) { nh = scan->right; break; }
            scan = scan->next;
        }
        head = nh;
    }
    return h;
}

int main(void) {
    long long acc = 0;
    for (long long rep = 0; rep < 16000; rep++) {
        long long base = acc % 100;
        Node *root = build_bst(500, base);
        connect(root);
        long long h = level_hash(root);
        acc = (acc * 131 + h) % MOD;
        free_tree(root);
    }
    printf("%lld\n", acc);
    return 0;
}
