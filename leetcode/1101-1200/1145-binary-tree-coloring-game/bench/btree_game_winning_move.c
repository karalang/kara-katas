// LeetCode #1145: Binary Tree Coloring Game -- the C mirror of
// btree_game_winning_move.kara: one walk counting every subtree; at the
// first player's node its two sides and the rest of the tree are the
// three parts blue can take, and blue wins when one holds more than half.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t count(const TreeNode *node, int64_t x, int64_t *l_out, int64_t *r_out) {
    if (!node) return 0;
    int64_t l = count(node->left, x, l_out, r_out);
    int64_t r = count(node->right, x, l_out, r_out);
    if (node->val == x) {
        *l_out = l;
        *r_out = r;
    }
    return l + r + 1;
}

static int btree_game_winning_move(const TreeNode *root, int64_t n, int64_t x) {
    int64_t l = 0, r = 0;
    count(root, x, &l, &r);
    int64_t above = n - 1 - l - r;
    int64_t most = l > r ? l : r;
    if (above > most) most = above;
    return most * 2 > n;
}

static int64_t seed = 1145;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static TreeNode *leaf(int32_t v) {
    TreeNode *n = malloc(sizeof *n);
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

static TreeNode *random_tree(int64_t count_) {
    int32_t pool[100];
    for (int64_t i = 0; i < count_; i++) pool[i] = (int32_t)(i + 1);
    for (int64_t j = count_ - 1; j >= 1; j--) {
        int64_t k = next_random() % (j + 1);
        int32_t t = pool[j];
        pool[j] = pool[k];
        pool[k] = t;
    }
    TreeNode *nodes[100];
    nodes[0] = leaf(pool[0]);
    for (int64_t i = 1; i < count_; i++) {
        TreeNode *c = leaf(pool[i]);
        for (;;) {
            TreeNode *at = nodes[next_random() % i];
            if (next_random() % 2 == 0) {
                if (!at->left) { at->left = c; break; }
            } else if (!at->right) {
                at->right = c;
                break;
            }
        }
        nodes[i] = c;
    }
    return nodes[0];
}

int main(void) {
    // 20 trees of 99 nodes, built once. Each of 1000 rounds asks every tree
    // about 99 first moves drawn at random.
    TreeNode *trees[20];
    for (int t = 0; t < 20; t++) trees[t] = random_tree(99);
    int64_t wins = 0, check = 0;
    for (int r = 0; r < 1000; r++) {
        for (int t = 0; t < 20; t++) {
            for (int k = 0; k < 99; k++) {
                int64_t x = next_random() % 99 + 1;
                int answer = btree_game_winning_move(trees[t], 99, x);
                wins += answer;
                check = (check * 31 + x + answer) % 1000000007;
            }
        }
    }
    printf("1000 rounds over 20 trees of 99 nodes: blue wins %lld, checksum %lld\n",
           (long long)wins, (long long)check);
    return 0;
}
