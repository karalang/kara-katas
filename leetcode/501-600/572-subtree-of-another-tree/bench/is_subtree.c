// Benchmark for #572: C mirror of the ★ arm (recursion); see
// is_subtree.kara. Nodes are `malloc`'d and reached through plain
// pointers, with no counts.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int same_tree(const TreeNode *a, const TreeNode *b) {
    if (a == NULL && b == NULL) {
        return 1;
    }
    if (a != NULL && b != NULL) {
        return a->val == b->val && same_tree(a->left, b->left) && same_tree(a->right, b->right);
    }
    return 0;
}

static int is_subtree(const TreeNode *root, const TreeNode *sub_root) {
    if (same_tree(root, sub_root)) {
        return 1;
    }
    if (root == NULL) {
        return 0;
    }
    return is_subtree(root->left, sub_root) || is_subtree(root->right, sub_root);
}

// ---- benchmark --------------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static TreeNode *leaf(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = NULL;
    n->right = NULL;
    return n;
}

static TreeNode *random_tree(int64_t size, int64_t *seed) {
    TreeNode *root = leaf(next_random(seed) % 2);
    for (int64_t i = 1; i < size; i++) {
        TreeNode *c = leaf(next_random(seed) % 2);
        TreeNode *node = root;
        for (;;) {
            if (next_random(seed) % 2 == 0) {
                if (node->left != NULL) {
                    node = node->left;
                } else {
                    node->left = c;
                    break;
                }
            } else {
                if (node->right != NULL) {
                    node = node->right;
                } else {
                    node->right = c;
                    break;
                }
            }
        }
    }
    return root;
}

static TreeNode *copy_tree(const TreeNode *node) {
    if (node == NULL) {
        return NULL;
    }
    TreeNode *n = leaf(node->val);
    n->left = copy_tree(node->left);
    n->right = copy_tree(node->right);
    return n;
}

static void all_nodes(TreeNode *node, TreeNode **out, int64_t *len) {
    if (node != NULL) {
        out[(*len)++] = node;
        all_nodes(node->left, out, len);
        all_nodes(node->right, out, len);
    }
}

static void free_tree(TreeNode *node) {
    if (node != NULL) {
        free_tree(node->left);
        free_tree(node->right);
        free(node);
    }
}

int main(void) {
    int64_t count = 20;
    int64_t rounds = 1000;
    int64_t seed = 572;
    TreeNode *roots[20];
    TreeNode *subs[20];
    TreeNode **nodes = malloc(2000 * sizeof(TreeNode *));
    TreeNode **inside = malloc(2000 * sizeof(TreeNode *));
    for (int64_t g = 0; g < count; g++) {
        TreeNode *root = random_tree(2000, &seed);
        int64_t len = 0;
        all_nodes(root, nodes, &len);
        TreeNode *picked;
        for (;;) {
            picked = nodes[next_random(&seed) % len];
            int64_t in = 0;
            all_nodes(picked, inside, &in);
            if (in >= 20) {
                break;
            }
        }
        TreeNode *sub = copy_tree(picked);
        if (g % 2 == 1) {
            int64_t in = 0;
            all_nodes(sub, inside, &in);
            TreeNode *n = inside[next_random(&seed) % in];
            n->val = 1 - n->val;
        }
        roots[g] = root;
        subs[g] = sub;
    }
    int64_t found = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int got = is_subtree(roots[p], subs[p]);
            if (got) {
                found += 1;
            }
            checksum = (checksum * 31 + (got ? g + 2 : 1)) % 1000000007;
        }
    }
    printf("%lld pairs, %lld rounds: %lld found, checksum %lld\n", (long long)count,
           (long long)rounds, (long long)found, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free_tree(roots[g]);
        free_tree(subs[g]);
    }
    free(nodes);
    free(inside);
    return 0;
}
