// LeetCode #2487: Remove Nodes From Linked List -- C mirror of the ★ arm's
// benchmark (remove.kara): the same 22000 lists of `malloc`'d nodes, each
// cleared by the same stack, an array of node pointers; a popped node is
// freed, and the kept ones after they are folded into the checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *stack[1000];

static ListNode *remove_nodes(ListNode *head) {
    int64_t top = 0;
    ListNode *cur = head;
    while (cur != NULL) {
        ListNode *node = cur;
        cur = node->next;
        while (top > 0 && stack[top - 1]->val < node->val) {
            free(stack[--top]);
        }
        stack[top++] = node;
    }
    ListNode *result = NULL;
    while (top > 0) {
        ListNode *node = stack[--top];
        node->next = result;
        result = node;
    }
    return result;
}

static ListNode *build(int64_t m, int64_t round, int64_t check) {
    ListNode *head = NULL;
    for (int64_t j = m - 1; j >= 0; j--) {
        ListNode *node = malloc(sizeof(ListNode));
        node->val = (m - j) * 10 + (round * 7919 + j * 104729 + check) % 37;
        node->next = head;
        head = node;
    }
    return head;
}

int main(void) {
    int64_t rounds = 22000, kept = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        ListNode *cur = remove_nodes(build(1000, r, check));
        while (cur != NULL) {
            kept++;
            check = (check * 31 + cur->val) % 1000000007;
            ListNode *next = cur->next;
            free(cur);
            cur = next;
        }
    }
    printf("%lld lists of 1000 nodes: %lld kept, checksum %lld\n", (long long)rounds, (long long)kept, (long long)check);
    return 0;
}
