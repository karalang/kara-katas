// LeetCode #1612: Check If Two Expression Trees are Equivalent -- the bench
// in C, mirroring equivalent.kara: one walk counts the first tree's leaves
// up and the second's down, into one array of 26 counts. Each node is its
// own malloc.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    char val;
    struct Node *left, *right;
} Node;

static void tally(const Node *node, int sign, int32_t counts[26]) {
    if (!node) return;
    if (node->val == '+') {
        tally(node->left, sign, counts);
        tally(node->right, sign, counts);
    } else {
        counts[node->val - 'a'] += sign;
    }
}

static bool check_equivalence(const Node *root1, const Node *root2) {
    int32_t counts[26] = {0};
    tally(root1, 1, counts);
    tally(root2, -1, counts);
    for (int i = 0; i < 26; i++)
        if (counts[i] != 0) return false;
    return true;
}

static int64_t seed = 1612;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t big(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static Node *node(char c, Node *l, Node *r) {
    Node *n = malloc(sizeof(Node));
    n->val = c;
    n->left = l;
    n->right = r;
    return n;
}

static Node *random_expression(const char *leaves, int64_t n) {
    Node **loose = malloc(n * sizeof(Node *));
    int64_t len = n;
    for (int64_t i = 0; i < n; i++) loose[i] = node(leaves[i], NULL, NULL);
    while (len > 1) {
        int64_t i = big() % len;
        Node *a = loose[i];
        loose[i] = loose[--len];
        int64_t j = big() % len;
        Node *b = loose[j];
        loose[j] = loose[--len];
        loose[len++] = node('+', a, b);
    }
    Node *root = loose[0];
    free(loose);
    return root;
}

static void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

#define N 50000

int main(void) {
    Node *ones[10], *twos[10];
    char *leaves = malloc(N), *other = malloc(N);
    for (int p = 0; p < 10; p++) {
        for (int i = 0; i < N; i++) leaves[i] = (char)('a' + next_random() % 26);
        for (int i = 0; i < N; i++) other[i] = leaves[i];
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = big() % (i + 1);
            char t = other[i];
            other[i] = other[j];
            other[j] = t;
        }
        if (next_random() % 2 == 0) {
            int64_t i = big() % N;
            other[i] = (char)('a' + next_random() % 26);
        }
        ones[p] = random_expression(leaves, N);
        twos[p] = random_expression(other, N);
    }
    int64_t check = 0, equivalent = 0;
    for (int p = 0; p < 10; p++) {
        for (int k = 0; k < 10; k++) {
            bool same = k % 2 == 0 ? check_equivalence(ones[p], twos[p]) : check_equivalence(twos[p], ones[p]);
            if (same) equivalent++;
            check = (check * 31 + (same ? 1 : 0) + 1) % 1000000007;
        }
    }
    printf("10 pairs of 50000 leaves from 26 letters, 100 checks: %lld equivalent, checksum %lld\n",
           (long long)equivalent, (long long)check);
    for (int p = 0; p < 10; p++) {
        free_tree(ones[p]);
        free_tree(twos[p]);
    }
    free(leaves);
    free(other);
    return 0;
}
