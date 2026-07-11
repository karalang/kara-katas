/*
 * Benchmark workload — Reverse Linked List II (LeetCode #92).
 * C mirror of bench/reverse_between.kara. Plain malloc/free singly-linked list — the
 * raw-pointer metal floor against Kara's shared struct and Rust's Rc<RefCell<>>. Each
 * iteration builds a fresh M=200 list, reverses a ~100-node window (shifting start),
 * folds the result and frees. Same M/K. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *reverse_between(ListNode *head, int64_t left, int64_t right) {
    ListNode dummy;
    dummy.next = head;
    ListNode *prev = &dummy;
    for (int64_t i = 1; i < left; i++)
        if (prev->next) prev = prev->next;
    ListNode *cur = prev->next;
    if (cur) {
        for (int64_t j = left; j < right; j++) {
            ListNode *nxt = cur->next;
            if (nxt) {
                cur->next = nxt->next;
                nxt->next = prev->next;
                prev->next = nxt;
            }
        }
    }
    return dummy.next;
}

static ListNode *build(int64_t m, int64_t seed) {
    ListNode dummy;
    dummy.next = NULL;
    ListNode *tail = &dummy;
    for (int64_t j = 0; j < m; j++) {
        ListNode *node = (ListNode *)malloc(sizeof(ListNode));
        node->val = (j + seed) % 1000;
        node->next = NULL;
        tail->next = node;
        tail = node;
    }
    return dummy.next;
}

static int64_t fold_and_free(ListNode *list, int64_t seed) {
    int64_t a = seed;
    ListNode *c = list;
    while (c) {
        a = (a * 131 + (c->val + 1000)) % 1000000007;
        ListNode *next = c->next;
        free(c);
        c = next;
    }
    return a;
}

int main(void) {
    const int64_t m = 200, total = 178000, modulus = 1000000007;
    int64_t sum = 0;
    for (int64_t k = 0; k < total; k++) {
        ListNode *list = build(m, k);
        int64_t left = 1 + (k % 50);
        int64_t right = left + 100;
        ListNode *r = reverse_between(list, left, right);
        sum = (sum * 131 + fold_and_free(r, k)) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
