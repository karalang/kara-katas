// LeetCode #894 bench: the ★ arm (recursion with a memo, the trees sharing
// their subtrees) asked 1,500 times for every full tree of 19 nodes; each
// tree is walked in preorder into a checksum. The same algorithm as
// all_possible_fbt.kara. Nodes are malloc'd one at a time and, since the
// trees share them, freed together at the end of each call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

typedef struct {
    Node **items;
    int64_t len, cap;
} List;

static void push(List *l, Node *n) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof(Node *));
    }
    l->items[l->len++] = n;
}

static List copy(const List *l) {
    List c = {malloc((l->len ? l->len : 1) * sizeof(Node *)), l->len, l->len ? l->len : 1};
    memcpy(c.items, l->items, l->len * sizeof(Node *));
    return c;
}

// every node made in this call, to free together
static List made;

static Node *new_node(Node *left, Node *right) {
    Node *n = malloc(sizeof(Node));
    n->val = 0;
    n->left = left;
    n->right = right;
    push(&made, n);
    return n;
}

static List memo[21];
static int known[21];

static List build(int64_t n) {
    if (known[n]) return copy(&memo[n]);
    List out = {0};
    if (n == 1) {
        push(&out, new_node(NULL, NULL));
    } else if (n % 2 == 1) {
        for (int64_t left = 1; left < n - 1; left += 2) {
            List lefts = build(left);
            List rights = build(n - 1 - left);
            for (int64_t i = 0; i < lefts.len; i++)
                for (int64_t j = 0; j < rights.len; j++) push(&out, new_node(lefts.items[i], rights.items[j]));
            free(lefts.items);
            free(rights.items);
        }
    }
    memo[n] = copy(&out);
    known[n] = 1;
    return out;
}

static List all_possible_fbt(int64_t n) {
    for (int i = 0; i < 21; i++) {
        if (known[i]) free(memo[i].items);
        known[i] = 0;
    }
    return build(n);
}

// the tree's preorder code, 1 for a node with children and 0 for a leaf,
// folded into a hash
static int64_t code(Node *node, int64_t h) {
    if (!node) return h;
    if (!node->left) return h * 3 % 1000000007;
    return code(node->right, code(node->left, (h * 3 + 1) % 1000000007));
}

int main(void) {
    int64_t trees = 0, check = 0;
    for (int c = 0; c < 1500; c++) {
        List all = all_possible_fbt(19);
        trees += all.len;
        for (int64_t i = 0; i < all.len; i++) check = (check * 131 + code(all.items[i], 1)) % 1000000007;
        free(all.items);
        for (int64_t i = 0; i < made.len; i++) free(made.items[i]);
        made.len = 0;
    }
    printf("1500 calls for 19 nodes: %lld trees, checksum %lld\n", (long long)trees, (long long)check);
    return 0;
}
