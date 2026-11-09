// LeetCode #2046 -- the ★ arm as a benchmark; mirror of sort.kara, the
// nodes malloc'd one by one and freed after each round.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *sort_linked_list(ListNode *head) {
    if (!head) return NULL;
    ListNode *front = head, *prev = head, *cur = head->next;
    while (cur) {
        ListNode *node = cur;
        cur = node->next;
        if (node->val < 0) {
            prev->next = node->next;
            node->next = front;
            front = node;
        } else {
            prev = node;
        }
    }
    return front;
}

static ListNode *build(int64_t m, int64_t round) {
    ListNode *head = NULL;
    for (int64_t j = m - 1; j >= 0; j--) {
        ListNode *n = malloc(sizeof *n);
        n->val = (7 * j + round) % 3 == 0 ? -(j / 2) : j / 2;
        n->next = head;
        head = n;
    }
    return head;
}

int main(void) {
    int64_t rounds = 20000, m = 1000, negatives = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        ListNode *cur = sort_linked_list(build(m, r));
        while (cur) {
            if (cur->val < 0) negatives++;
            check = (check * 31 + cur->val + 1000) % 1000000007;
            ListNode *next = cur->next;
            free(cur);
            cur = next;
        }
    }
    printf("%lld rounds: %lld negatives, checksum %lld\n", (long long)rounds,
           (long long)negatives, (long long)check);
    return 0;
}
