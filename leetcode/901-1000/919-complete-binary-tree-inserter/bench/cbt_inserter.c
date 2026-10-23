// LeetCode #919: Complete Binary Tree Inserter -- bench: a queue of the
// nodes with a free child slot. Mirrors cbt_inserter.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

// The queue is a ring over an array that grows when full.
typedef struct {
    TreeNode *root;
    TreeNode **open;
    int64_t head, len, cap;
} CBTInserter;

static TreeNode *new_node(int64_t val) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = val;
    t->left = NULL;
    t->right = NULL;
    return t;
}

static void push_back(CBTInserter *c, TreeNode *t) {
    if (c->len == c->cap) {
        int64_t cap = c->cap ? 2 * c->cap : 8;
        TreeNode **open = malloc(cap * sizeof(TreeNode *));
        for (int64_t i = 0; i < c->len; i++) open[i] = c->open[(c->head + i) % c->cap];
        free(c->open);
        c->open = open;
        c->head = 0;
        c->cap = cap;
    }
    c->open[(c->head + c->len) % c->cap] = t;
    c->len++;
}

static CBTInserter cbt_new(TreeNode *root) {
    CBTInserter c = {root, NULL, 0, 0, 0};
    TreeNode **walk = malloc(8 * sizeof(TreeNode *));
    int64_t cap = 8, front = 0, back = 0;
    walk[back++] = root;
    while (front < back) {
        TreeNode *node = walk[front++];
        if (back + 2 > cap) {
            cap *= 2;
            walk = realloc(walk, cap * sizeof(TreeNode *));
        }
        if (node->left) walk[back++] = node->left;
        if (node->right) walk[back++] = node->right;
        if (!node->left || !node->right) push_back(&c, node);
    }
    free(walk);
    return c;
}

static int64_t cbt_insert(CBTInserter *c, int64_t val) {
    TreeNode *child = new_node(val);
    TreeNode *parent = c->open[c->head];
    if (!parent->left) {
        parent->left = child;
    } else {
        parent->right = child;
        c->head = (c->head + 1) % c->cap;
        c->len--;
    }
    push_back(c, child);
    return parent->val;
}

static void free_tree(TreeNode *t) {
    if (!t) return;
    free_tree(t->left);
    free_tree(t->right);
    free(t);
}

static int64_t seed = 919;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// A complete tree holding vals in level order.
static TreeNode *complete_tree(const int64_t *vals, int64_t n) {
    TreeNode **nodes = malloc(n * sizeof(TreeNode *));
    for (int64_t i = 0; i < n; i++) nodes[i] = new_node(vals[i]);
    for (int64_t i = 1; i < n; i++) {
        TreeNode *parent = nodes[(i - 1) / 2];
        if (i % 2 == 1) parent->left = nodes[i];
        else parent->right = nodes[i];
    }
    TreeNode *root = nodes[0];
    free(nodes);
    return root;
}

int main(void) {
    const int64_t rounds = 200, n = 1000, m = 50000;
    int64_t total = 0, check = 0;
    int64_t *vals = malloc(n * sizeof(int64_t));
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < n; i++) vals[i] = next_random() % 100000;
        CBTInserter c = cbt_new(complete_tree(vals, n));
        int64_t parents = 0;
        for (int64_t j = 0; j < m; j++) parents += cbt_insert(&c, next_random() % 100000);
        TreeNode *root = c.root;
        total += parents;
        check = (check * 1000003 + parents + root->val) % 1000000007;
        free(c.open);
        free_tree(root);
    }
    free(vals);
    printf("%lld rounds of %lld inserts into trees of %lld: parents summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)m, (long long)n, (long long)total, (long long)check);
    return 0;
}
