// LeetCode #876 bench: C mirror of middle_node.kara (the ★ arm, slow and
// fast pointers) on the same 2,000,000 searches, each node malloc'd.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct ListNode {
    int64_t val;
    struct ListNode *next;
};

static struct ListNode *middle_node(struct ListNode *head) {
    struct ListNode *slow = head, *fast = head;
    while (fast != NULL) {
        struct ListNode *after = fast->next;
        if (after == NULL) break;
        fast = after->next;
        if (slow != NULL) slow = slow->next;
    }
    return slow;
}

static int64_t seed = 876;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static struct ListNode *from_values(const int64_t *values, int n) {
    struct ListNode *head = NULL;
    for (int k = n - 1; k >= 0; k--) {
        struct ListNode *node = malloc(sizeof *node);
        node->val = values[k];
        node->next = head;
        head = node;
    }
    return head;
}

int main(void) {
    struct ListNode *lists[2000];
    int64_t values[100];
    for (int i = 0; i < 2000; i++) {
        int n = (int)(next_random() % 100 + 1);
        for (int j = 0; j < n; j++) values[j] = next_random() % 100 + 1;
        lists[i] = from_values(values, n);
    }
    int64_t total = 0, check = 0;
    for (int64_t k = 0; k < 2000000; k++) {
        struct ListNode *m = middle_node(lists[(k * 7 + k / 2000) % 2000]);
        if (m != NULL) {
            total += m->val;
            check = (check * 131 + m->val) % 1000000007;
        }
    }
    printf("2000000 searches over 2000 lists: middle values sum to %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int i = 0; i < 2000; i++) {
        struct ListNode *cur = lists[i];
        while (cur != NULL) {
            struct ListNode *next = cur->next;
            free(cur);
            cur = next;
        }
    }
    return 0;
}
