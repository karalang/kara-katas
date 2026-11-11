// LeetCode #1120: Maximum Average Subtree -- the bench in C, the ★ arm
// over `malloc`ed nodes, the same 16 trees and 200 rounds.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct Node {
    int32_t val;
    struct Node *left, *right;
} Node;

static void walk(const Node *n, double *best, int64_t *sum, int64_t *count) {
    if (!n) {
        *sum = 0;
        *count = 0;
        return;
    }
    int64_t ls, lc, rs, rc;
    walk(n->left, best, &ls, &lc);
    walk(n->right, best, &rs, &rc);
    *sum = ls + rs + n->val;
    *count = lc + rc + 1;
    double average = (double)*sum / (double)*count;
    if (average > *best) *best = average;
}

static double maximum_average_subtree(const Node *root) {
    double best = 0.0;
    int64_t s, c;
    walk(root, &best, &s, &c);
    return best;
}

static int64_t seed = 1120;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int32_t random_value(void) {
    int64_t hi = next_random();
    int64_t lo = next_random();
    return (int32_t)((hi * 32768 + lo) % 100001);
}

static Node *new_node(int32_t v) {
    Node *n = malloc(sizeof(Node));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

int main(void) {
    static Node *trees[16][10000];
    for (int j = 0; j < 16; j++) {
        trees[j][0] = new_node(random_value());
        for (int i = 1; i < 10000; i++) {
            Node *c = new_node(random_value());
            for (;;) {
                Node *at = trees[j][next_random() % i];
                if (next_random() % 2 == 0) {
                    if (!at->left) { at->left = c; break; }
                } else if (!at->right) { at->right = c; break; }
            }
            trees[j][i] = c;
        }
    }
    double total = 0.0;
    int64_t check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int64_t j = 0; j < 16; j++) {
            int64_t at = (round * 7919 + j * 104729) % 10000;
            Node *n = trees[j][at];
            n->val = (int32_t)(((int64_t)n->val * 7 + round) % 100001);
            double answer = maximum_average_subtree(trees[j][0]);
            total += answer;
            check = (check * 31 + (int64_t)(answer * 1000.0)) % 1000000007;
        }
    }
    printf("200 rounds over 16 trees of 10^4 nodes: answers total %.3f, checksum %lld\n", total, (long long)check);
    for (int j = 0; j < 16; j++)
        for (int i = 0; i < 10000; i++) free(trees[j][i]);
    return 0;
}
