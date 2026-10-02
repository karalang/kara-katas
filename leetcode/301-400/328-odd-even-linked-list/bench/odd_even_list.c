// Benchmark workload for LeetCode #328 — C mirror of odd_even_list.kara.
//
// Same workload: a list of LEN nodes built once, then PUNCHES punches, each
// regrouping the list in place and walking it once to fold a rolling hash
// and replace one value. Nodes are malloc'd one at a time, as the Kāra arm
// allocates them, and never freed: the process exits right after.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 1000000
#define PUNCHES 10
#define MODULUS 1073741789LL

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *odd_even_list(ListNode *head) {
    if (head == NULL || head->next == NULL) {
        return head;
    }
    ListNode *first = head, *second = head->next;
    ListNode *odd = first, *even = second;
    for (;;) {
        ListNode *n = even->next;
        if (n == NULL) {
            break;
        }
        odd->next = n;
        odd = n;
        even->next = n->next;
        if (n->next == NULL) {
            break;
        }
        even = n->next;
    }
    odd->next = second;
    return first;
}

static int64_t seed = 328;

static int64_t next_rand(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    ListNode *head = NULL;
    for (int64_t i = 0; i < LEN; i++) {
        int64_t hi = next_rand();
        int64_t lo = next_rand();
        ListNode *node = malloc(sizeof(ListNode));
        node->val = (hi * 32768 + lo) % 1000000;
        node->next = head;
        head = node;
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        head = odd_even_list(head);
        int64_t hi = next_rand();
        int64_t lo = next_rand();
        int64_t pos = (hi * 32768 + lo) % LEN;
        hi = next_rand();
        lo = next_rand();
        int64_t fresh = (hi * 32768 + lo) % 1000000;
        int64_t k = 0;
        for (ListNode *n = head; n != NULL; n = n->next) {
            if (k == pos) {
                n->val = fresh;
            }
            sink = (sink * 31 + n->val * (k + 1)) % MODULUS;
            k++;
        }
    }
    printf("sink %lld\n", (long long)sink);
    return 0;
}
