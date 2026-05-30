/*
 * Benchmark workload — Merge Two Sorted Lists (LeetCode #21), iterative.
 * C mirror of bench/iterative.kara. Plain malloc/free linked list — Kāra's
 * `shared struct` and Rust's `Rc<RefCell<>>` are single-owner in this workload
 * (two lists per iteration, merged then freed at iteration end), so the C
 * mirror expresses the same alloc-per-node build + in-place re-link + drop
 * shape without RC overhead — the cleanest LLVM-backend floor.
 *
 * Same N/K, evens/odds interleaving, and full-traversal sink. The merged list
 * is freed after the sink read. See ../README.md § Benchmarks.
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

static ListNode *merge_two_lists(ListNode *l1, ListNode *l2) {
    ListNode dummy;
    dummy.val = 0;
    dummy.next = NULL;
    ListNode *tail = &dummy;
    ListNode *a = l1;
    ListNode *b = l2;
    while (a && b) {
        if (a->val <= b->val) {
            tail->next = a;
            tail = a;
            a = a->next;
        } else {
            tail->next = b;
            tail = b;
            b = b->next;
        }
    }
    tail->next = a ? a : b;
    return dummy.next;
}

static ListNode *build_list(int64_t start, int64_t step, int64_t count) {
    if (count <= 0) return NULL;
    ListNode *head = node_new(start);
    ListNode *tail = head;
    int64_t v = start;
    for (int64_t i = 1; i < count; i++) {
        v += step;
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
        ListNode *a = build_list(0, 2, n_values);
        ListNode *b = build_list(1, 2, n_values);
        ListNode *merged = merge_two_lists(a, b);
        total += sum_list(merged);
        chain_free(merged);
    }
    printf("%lld\n", (long long)total);
    return 0;
}
