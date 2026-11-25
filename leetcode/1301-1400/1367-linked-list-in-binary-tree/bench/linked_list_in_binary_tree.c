// LeetCode #1367 bench -- C: every tree node tried as the start of the
// list, and from each the list matched down the tree, either child
// carrying the next value.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TREES 20
#define NODES 2500

typedef struct ListNode {
    int val;
    struct ListNode *next;
} ListNode;

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

// the list from `head` on read down from `node`
static bool matches_from(const ListNode *head, const TreeNode *node) {
    if (!head) return true;
    if (!node) return false;
    return head->val == node->val && (matches_from(head->next, node->left) || matches_from(head->next, node->right));
}

static bool is_sub_path(const ListNode *head, const TreeNode *root) {
    if (!root) return false;
    return matches_from(head, root) || is_sub_path(head, root->left) || is_sub_path(head, root->right);
}

static int64_t seed = 1367;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    TreeNode *node;
    bool left;
} Place;

static TreeNode *new_node(void) {
    TreeNode *n = malloc(sizeof *n);
    n->val = (int)(1 + next_random() % 2);
    n->left = n->right = NULL;
    return n;
}

int main(void) {
    // 20 trees of 2500 nodes valued 1 or 2, the constraints' most nodes,
    // each node hung on a random empty child place, built once; then 20000
    // rounds, each flipping one node's value and searching that tree for a
    // list of 8 to 15 values, all drawn from the checksum so far
    static TreeNode *trees[TREES][NODES];
    static Place places[NODES + 1];
    for (int t = 0; t < TREES; t++) {
        TreeNode *root = new_node();
        trees[t][0] = root;
        size_t count = 0;
        places[count++] = (Place){root, true};
        places[count++] = (Place){root, false};
        for (int i = 1; i < NODES; i++) {
            int64_t k = next_random() % (int64_t)count;
            Place p = places[k];
            places[k] = places[--count];
            TreeNode *node = new_node();
            if (p.left) {
                p.node->left = node;
            } else {
                p.node->right = node;
            }
            places[count++] = (Place){node, true};
            places[count++] = (Place){node, false};
            trees[t][i] = node;
        }
    }
    int64_t check = 0;
    int hits = 0;
    for (int64_t r = 0; r < 20000; r++) {
        TreeNode **nodes = trees[check % 20];
        TreeNode *flipped = nodes[(check / 20) % 2500];
        flipped->val = 3 - flipped->val;
        int64_t m = 8 + check % 8;
        int64_t bits = check / 7;
        ListNode *head = NULL;
        for (int64_t k = 0; k < m; k++) {
            ListNode *l = malloc(sizeof *l);
            l->val = (int)(1 + (bits >> k) % 2);
            l->next = head;
            head = l;
        }
        bool found = is_sub_path(head, nodes[0]);
        while (head) {
            ListNode *next = head->next;
            free(head);
            head = next;
        }
        if (found) hits++;
        check = (check * 31 + m * 2 + (found ? 1 : 0) + r) % 1000000007;
    }
    printf("20000 rounds over 20 trees of 2500 nodes: %d found, checksum %lld\n", hits, (long long)check);
    return 0;
}
