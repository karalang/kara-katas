/*
 * Benchmark workload — Remove Duplicates from Sorted List II (LeetCode #82).
 * C mirror of bench/remove_duplicates_ii_list.kara. Plain malloc/free singly-linked
 * list — the nodes are single-owner in this workload (built, deduped, then freed at
 * iteration end), so the raw-pointer list is the honest metal floor against Kāra's
 * `shared struct` and Rust's `Rc<RefCell<>>`. Each iteration builds a fresh list,
 * runs delete_duplicates (freeing the nodes it drops), folds the survivors through a
 * rolling polynomial hash, then frees the rest. Same M/K and even-duplicated/
 * odd-single pattern. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *node_new(int64_t val) {
    ListNode *p = (ListNode *)malloc(sizeof(ListNode));
    p->val = val;
    p->next = NULL;
    return p;
}

static ListNode *delete_duplicates(ListNode *head) {
    ListNode dummy;
    dummy.val = 0;
    dummy.next = head;
    ListNode *prev = &dummy;
    ListNode *cur = dummy.next;
    while (cur != NULL) {
        int is_dup = (cur->next != NULL && cur->val == cur->next->val);
        if (is_dup) {
            int64_t v = cur->val;
            ListNode *runner = cur;
            while (runner != NULL && runner->val == v) {
                ListNode *nxt = runner->next;
                free(runner);           /* single-owner: reclaim the dropped run */
                runner = nxt;
            }
            prev->next = runner;
            cur = runner;
        } else {
            prev = cur;
            cur = cur->next;
        }
    }
    return dummy.next;
}

/* Sorted list: even values duplicated (removed by #82), odd values single (kept). */
static ListNode *build(int64_t m) {
    ListNode dummy;
    dummy.next = NULL;
    ListNode *tail = &dummy;
    for (int64_t v = 0; v < m; v++) {
        ListNode *node = node_new(v);
        tail->next = node;
        tail = node;
        if (v % 2 == 0) {
            ListNode *d = node_new(v);
            tail->next = d;
            tail = d;
        }
    }
    return dummy.next;
}

static int64_t fold_and_free(ListNode *list, int64_t seed) {
    int64_t a = seed;
    ListNode *c = list;
    while (c != NULL) {
        a = (a * 131 + (c->val + 1000)) % 1000000007;
        ListNode *next = c->next;
        free(c);
        c = next;
    }
    return a;
}

int main(void) {
    const int64_t m = 300, total = 61000, modulus = 1000000007;
    int64_t sum = 0;
    for (int64_t k = 0; k < total; k++) {
        ListNode *list = build(m);
        ListNode *dedup = delete_duplicates(list);
        sum = (sum * 131 + fold_and_free(dedup, k)) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
