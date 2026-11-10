// LeetCode #2058: Find the Minimum and Maximum Number of Nodes Between
// Critical Points -- C mirror of the ★ arm's benchmark (critical.kara): the
// same 50 lists of 100000 values, each built node by node with `malloc`,
// answered by one walk, and freed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static int64_t seed = 2058;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void nodes_between_critical_points(const ListNode *head, int64_t out[2]) {
    out[0] = out[1] = -1;
    if (!head) {
        return;
    }
    int64_t before = head->val, at = 1, first = -1, last = -1, nearest = -1;
    for (const ListNode *node = head->next; node; node = node->next, at++) {
        const ListNode *after = node->next;
        if (after) {
            int64_t v = node->val;
            if ((v > before && v > after->val) || (v < before && v < after->val)) {
                if (first < 0) {
                    first = at;
                } else if (nearest < 0 || at - last < nearest) {
                    nearest = at - last;
                }
                last = at;
            }
        }
        before = node->val;
    }
    if (nearest >= 0) {
        out[0] = nearest;
        out[1] = last - first;
    }
}

int main(void) {
    const int64_t tops[4] = {2, 3, 10, 100000};
    int64_t total = 0, check = 0;
    for (int t = 0; t < 50; t++) {
        int64_t top = tops[t % 4];
        ListNode *head = NULL;
        for (int i = 0; i < 100000; i++) {
            ListNode *node = malloc(sizeof *node);
            node->val = next_random() % top + 1;
            node->next = head;
            head = node;
        }
        int64_t d[2];
        nodes_between_critical_points(head, d);
        while (head) {
            ListNode *next = head->next;
            free(head);
            head = next;
        }
        total += d[0] + d[1];
        check = (check * 31 + d[0] + 2) % 1000000007;
        check = (check * 31 + d[1] + 2) % 1000000007;
    }
    printf("50 lists: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
