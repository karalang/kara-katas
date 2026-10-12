// Benchmark for #382: mirror of linked_list_random.kara (reservoir
// sampling over a singly linked list).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

typedef struct {
    ListNode *head;
    int64_t seed;
} Solution;

static int64_t below(Solution *s, int64_t n) {
    s->seed = (s->seed * 1103515245 + 12345) % 2147483648LL;
    return (s->seed / 65536) % n;
}

static int64_t get_random(Solution *s) {
    int64_t kept = 0, i = 0;
    for (ListNode *at = s->head; at; at = at->next) {
        i++;
        if (below(s, i) == 0) kept = at->val;
    }
    return kept;
}

int main(void) {
    int64_t seed = 7;
    ListNode *head = NULL;
    for (int k = 0; k < 10000; k++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        ListNode *n = malloc(sizeof *n);
        n->val = (seed / 65536) % 20001 - 10000;
        n->next = head;
        head = n;
    }
    Solution s = {head, 382};
    int64_t checksum = 0;
    for (int q = 0; q < 20000; q++)
        checksum = (checksum * 31 + get_random(&s) + 10000) % 1000000007;
    printf("checksum %lld\n", (long long)checksum);
    while (head) {
        ListNode *n = head->next;
        free(head);
        head = n;
    }
    return 0;
}
