/*
 * Benchmark workload — Partition List (LeetCode #86), SEQ lane.
 * C mirror of bench/partition_list.kara. Plain malloc/free singly-linked list — the
 * honest metal floor against Kāra's `shared struct` and Rust's `Rc<RefCell<>>`. Each
 * iteration builds a fresh M=200 list, stably partitions around x=50, adds the fold
 * into an associative sum, and frees the nodes. Same M/K. The partition_list_par.c
 * sibling parallelises the same reduction with pthreads. See ../README.md § Benchmarks.
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

static ListNode *partition(ListNode *head, int64_t x) {
    ListNode less_dummy, greater_dummy;
    less_dummy.next = NULL;
    greater_dummy.next = NULL;
    ListNode *less_tail = &less_dummy;
    ListNode *greater_tail = &greater_dummy;
    ListNode *cur = head;
    while (cur != NULL) {
        ListNode *nxt = cur->next;
        cur->next = NULL;
        if (cur->val < x) {
            less_tail->next = cur;
            less_tail = cur;
        } else {
            greater_tail->next = cur;
            greater_tail = cur;
        }
        cur = nxt;
    }
    less_tail->next = greater_dummy.next;
    return less_dummy.next;
}

static ListNode *build(int64_t m, int64_t seed) {
    ListNode dummy;
    dummy.next = NULL;
    ListNode *tail = &dummy;
    for (int64_t j = 0; j < m; j++) {
        ListNode *node = node_new((j * 7 + seed) % 100);
        tail->next = node;
        tail = node;
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
    const int64_t m = 200, total = 170000;
    int64_t sum = 0;
    for (int64_t k = 0; k < total; k++) {
        ListNode *list = build(m, k);
        ListNode *p = partition(list, 50);
        sum += fold_and_free(p, k);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
