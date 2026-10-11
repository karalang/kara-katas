// Benchmark for #369 -- mirror of plus_one.kara. The nodes are plain
// malloc'd structs; each list is freed once its checksum is taken.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *node(int64_t val, ListNode *next) {
    ListNode *n = malloc(sizeof *n);
    n->val = val;
    n->next = next;
    return n;
}

static ListNode *plus_one(ListNode *head) {
    ListNode *front = node(0, head);
    ListNode *last = front;
    for (ListNode *at = front->next; at; at = at->next)
        if (at->val != 9) last = at;
    last->val += 1;
    for (ListNode *rest = last->next; rest; rest = rest->next) rest->val = 0;
    if (front->val == 1) return front;
    free(front);
    return head;
}

int main(void) {
    int64_t seed = 369, total = 0, checksum = 0;
    for (int i = 0; i < 20; i++) {
        ListNode *head = NULL;
        for (int k = 0; k < 100000; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t d = (i % 2 == 0 && k < 50000) ? 9 : (seed / 65536) % 10;
            head = node(k == 99999 && d == 0 ? 1 : d, head);
        }
        for (int r = 0; r < 20; r++) head = plus_one(head);
        while (head) {
            total++;
            checksum = (checksum * 31 + head->val) % 1000000007;
            ListNode *next = head->next;
            free(head);
            head = next;
        }
    }
    printf("%lld digits, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
