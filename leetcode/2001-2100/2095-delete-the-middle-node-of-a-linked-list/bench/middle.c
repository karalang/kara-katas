// LeetCode #2095: Delete the Middle Node of a Linked List -- C mirror of
// the ★ arm's benchmark (middle.kara): the same 20000 lists of `malloc`'d
// nodes, each with its middle deleted 50 times by the same two runners,
// the deleted node freed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *delete_middle(ListNode *head) {
    if (head == NULL) return NULL;
    if (head->next == NULL) {
        free(head);
        return NULL;
    }
    ListNode *slow = head;
    ListNode *fast = head->next->next;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode *middle = slow->next;
    slow->next = middle->next;
    free(middle);
    return head;
}

static ListNode *build(int64_t m, int64_t round) {
    ListNode *head = NULL;
    for (int64_t j = m - 1; j >= 0; j--) {
        ListNode *node = malloc(sizeof(ListNode));
        node->val = (round * 7919 + j * 104729) % 100000 + 1;
        node->next = head;
        head = node;
    }
    return head;
}

int main(void) {
    int64_t rounds = 20000, left = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        ListNode *list = build(1000, r);
        for (int k = 0; k < 50; k++) list = delete_middle(list);
        while (list != NULL) {
            left++;
            check = (check * 31 + list->val) % 1000000007;
            ListNode *next = list->next;
            free(list);
            list = next;
        }
    }
    printf("%lld rounds: %lld nodes left, checksum %lld\n", (long long)rounds, (long long)left, (long long)check);
    return 0;
}
