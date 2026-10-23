// LeetCode #889 bench: recursion with a table of postorder positions, on
// 4000 random trees of 1,000 nodes, half of them full. The same algorithm
// as construct_from_pre_post.kara; nodes are malloc'd one at a time.
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
    n->left = n->right = NULL;
    return n;
}

static void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

// the subtree whose preorder is pre[lo..=hi] and whose postorder starts at
// post_lo
static Node *build(const int64_t *pre, const int64_t *at, int64_t lo, int64_t hi, int64_t post_lo) {
    if (lo > hi) return NULL;
    Node *node = new_node(pre[lo]);
    if (lo < hi) {
        int64_t size = at[pre[lo + 1]] - post_lo + 1;
        node->left = build(pre, at, lo + 1, lo + size, post_lo);
        node->right = build(pre, at, lo + size + 1, hi, post_lo + size);
    }
    return node;
}

static int64_t at_tab[1002];

static Node *construct_from_pre_post(const int64_t *pre, const int64_t *post, int64_t n) {
    for (int64_t i = 0; i < n; i++) at_tab[post[i]] = i;
    return build(pre, at_tab, 0, n - 1, 0);
}

static int64_t seed = 889;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t pre[1000], post[1000], npre, npost;

static void walk(Node *n) {
    if (!n) return;
    pre[npre++] = n->val;
    walk(n->left);
    walk(n->right);
    post[npost++] = n->val;
}

static Node *nodes[1000], *leaves[1000];

// as in the Kāra bench: a random tree of n nodes holding 1 to n
static Node *random_tree(int64_t n, int full) {
    int64_t vals[1000];
    for (int64_t v = 0; v < n; v++) vals[v] = v + 1;
    for (int64_t i = 1; i < n; i++) {
        int64_t j = next_random() % (i + 1);
        int64_t t = vals[i]; vals[i] = vals[j]; vals[j] = t;
    }
    int64_t count = 0;
    nodes[count++] = new_node(vals[0]);
    if (full) {
        int64_t nleaves = 0;
        leaves[nleaves++] = nodes[0];
        while (count + 2 <= n) {
            int64_t k = next_random() % nleaves;
            Node *leaf = leaves[k];
            leaves[k] = leaves[--nleaves];
            Node *a = new_node(vals[count]);
            Node *b = new_node(vals[count + 1]);
            leaf->left = a;
            leaf->right = b;
            nodes[count++] = a;
            nodes[count++] = b;
            leaves[nleaves++] = a;
            leaves[nleaves++] = b;
        }
    } else {
        for (int64_t k = 1; k < n; k++) {
            Node *node = new_node(vals[k]);
            for (;;) {
                Node *parent = nodes[next_random() % count];
                if (next_random() % 2 == 0) {
                    if (!parent->left) { parent->left = node; break; }
                } else if (!parent->right) {
                    parent->right = node;
                    break;
                }
            }
            nodes[count++] = node;
        }
    }
    return nodes[0];
}

static Node *queue[1000];

int main(void) {
    int64_t total = 0, check = 0;
    for (int c = 0; c < 4000; c++) {
        int full = c % 2 == 0;
        int64_t n = full ? 999 : 1000;
        Node *tree = random_tree(n, full);
        npre = npost = 0;
        walk(tree);
        Node *root = construct_from_pre_post(pre, post, n);
        // the rebuilt tree in level order, 0 for a missing child
        int64_t head = 0, tail = 0;
        if (root) {
            check = (check * 131 + root->val) % 1000000007;
            queue[tail++] = root;
        }
        while (head < tail) {
            Node *node = queue[head++];
            total++;
            if (node->left) {
                check = (check * 131 + node->left->val) % 1000000007;
                queue[tail++] = node->left;
            } else {
                check = check * 131 % 1000000007;
            }
            if (node->right) {
                check = (check * 131 + node->right->val) % 1000000007;
                queue[tail++] = node->right;
            } else {
                check = check * 131 % 1000000007;
            }
        }
        free_tree(tree);
        free_tree(root);
    }
    printf("4000 trees of up to 1000 nodes: %lld nodes rebuilt, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
