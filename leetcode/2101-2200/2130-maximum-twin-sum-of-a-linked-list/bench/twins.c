// LeetCode #2130: Maximum Twin Sum of a Linked List -- the benchmark, the
// same algorithm as twins.kara over malloc'd nodes; the values read into
// a growing array as the Kāra and Rust ones are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static int64_t seed = 2130;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t pair_sum(const ListNode *head) {
    size_t cap = 4, len = 0;
    int64_t *values = malloc(sizeof(int64_t) * cap);
    for (const ListNode *n = head; n; n = n->next) {
        if (len == cap) {
            cap *= 2;
            values = realloc(values, sizeof(int64_t) * cap);
        }
        values[len++] = n->val;
    }
    int64_t best = 0;
    for (size_t i = 0; i < len / 2; i++) {
        int64_t s = values[i] + values[len - 1 - i];
        if (s > best) best = s;
    }
    free(values);
    return best;
}

int main(void) {
    const int64_t n = 100000;
    ListNode *lists[10];
    for (int k = 0; k < 10; k++) {
        ListNode *head = NULL;
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = next_random();
            ListNode *node = malloc(sizeof(ListNode));
            node->val = (hi * 32768 + next_random()) % 100000 + 1;
            node->next = head;
            head = node;
        }
        lists[k] = head;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 50; round++) {
        for (int k = 0; k < 10; k++) {
            int64_t hi = next_random();
            int64_t at = (hi * 32768 + next_random()) % n;
            ListNode *node = lists[k];
            for (int64_t i = 0; i < at; i++) node = node->next;
            node->val = next_random() % 200000 + 1;
            int64_t sum = pair_sum(lists[k]);
            total += sum;
            check = (check * 31 + sum + round) % 1000000007;
        }
    }
    printf("500 solves: %lld in all, checksum %lld\n", (long long)total, (long long)check);
    for (int k = 0; k < 10; k++) {
        ListNode *n2 = lists[k];
        while (n2) {
            ListNode *next = n2->next;
            free(n2);
            n2 = next;
        }
    }
    return 0;
}
