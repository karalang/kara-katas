// LeetCode #2074: Reverse Nodes in Even Length Groups -- C mirror of the
// ★ arm's benchmark (groups.kara): 2000 rounds, each a fresh list of 10000
// values turned group by group in place, folded into a checksum and freed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *reverse_even_length_groups(ListNode *head) {
    if (!head) return NULL;
    ListNode *before = head;
    int64_t want = 2;
    while (before->next) {
        ListNode *start = before->next, *end = start, *cur = start;
        int64_t len = 0;
        while (len < want && cur) {
            len++;
            end = cur;
            cur = cur->next;
        }
        if (len % 2 == 0) {
            ListNode *turned = end->next, *rest = start;
            for (int64_t i = 0; i < len; i++) {
                ListNode *node = rest;
                rest = node->next;
                node->next = turned;
                turned = node;
            }
            before->next = turned;
            before = start;
        } else {
            before = end;
        }
        want++;
    }
    return head;
}

static ListNode *build(int64_t m, int64_t round) {
    ListNode *head = NULL;
    for (int64_t j = m - 1; j >= 0; j--) {
        ListNode *n = malloc(sizeof(ListNode));
        n->val = (j * 7919 + round) % 100001;
        n->next = head;
        head = n;
    }
    return head;
}

int main(void) {
    int64_t check = 0;
    for (int64_t r = 0; r < 2000; r++) {
        ListNode *cur = reverse_even_length_groups(build(10000 + r % 7, r));
        while (cur) {
            check = (check * 31 + cur->val) % 1000000007;
            ListNode *next = cur->next;
            free(cur);
            cur = next;
        }
    }
    printf("2000 rounds: checksum %lld\n", (long long)check);
    return 0;
}
