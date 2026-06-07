/*
 * Benchmark workload — Swap Nodes in Pairs (LeetCode #24), iterative.
 * C mirror of bench/iterative.kara. Plain malloc/free linked list — Kāra's
 * `shared struct` and Rust's `Rc<RefCell<>>` are single-owner in this workload
 * (one list per iteration, swapped then freed at iteration end), so the C
 * mirror expresses the same alloc-per-node build + in-place pair re-link +
 * drop shape without RC overhead — the cleanest LLVM-backend floor.
 *
 * Same N/K and full-traversal sink. The swapped list is freed after the sink
 * read. See ../README.md § Benchmarks.
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

static void chain_free(ListNode *head) {
    while (head) {
        ListNode *next = head->next;
        free(head);
        head = next;
    }
}

static ListNode *swap_pairs(ListNode *head) {
    ListNode dummy;
    dummy.val = 0;
    dummy.next = head;
    ListNode *prev = &dummy;
    while (prev->next && prev->next->next) {
        ListNode *first = prev->next;
        ListNode *second = first->next;
        /* Re-link prev → second → first → rest. */
        first->next = second->next;
        second->next = first;
        prev->next = second;
        prev = first;
    }
    return dummy.next;
}

static ListNode *build_list(int64_t count) {
    if (count <= 0) return NULL;
    ListNode *head = node_new(1);
    ListNode *tail = head;
    for (int64_t v = 2; v <= count; v++) {
        ListNode *node = node_new(v);
        tail->next = node;
        tail = node;
    }
    return head;
}

static int64_t sum_list(ListNode *list) {
    int64_t s = 0;
    for (ListNode *c = list; c; c = c->next) s += c->val;
    return s;
}

int main(void) {
    const int64_t n_values = 100;
    const int64_t k_iters = 500000;

    int64_t total = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        ListNode *list = build_list(n_values);
        ListNode *swapped = swap_pairs(list);
        total += sum_list(swapped);
        chain_free(swapped);
    }
    printf("%lld\n", (long long)total);
    return 0;
}
