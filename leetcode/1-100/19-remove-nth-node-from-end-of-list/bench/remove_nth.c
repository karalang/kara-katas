/*
 * Benchmark workload — Remove Nth Node From End (LeetCode #19).
 * C mirror of bench/remove_nth.kara. Plain malloc/free linked list — Kāra's
 * `shared struct` and Rust's `Rc<RefCell<>>` are single-owner in this
 * workload (one list per iteration, dropped at iteration end), so the C
 * mirror expresses the same alloc-per-node build + in-place splice + drop
 * shape without RC overhead — the cleanest LLVM-backend floor.
 *
 * Same N/K, append list-builder, rotating removal position, and sink. The
 * splice frees the removed node (the manual analogue of the removed Rc's
 * refcount hitting zero); the caller frees the remaining chain after the
 * sink read. See ../README.md § Benchmarks.
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

static ListNode *remove_nth_from_end(ListNode *head, int64_t n) {
    ListNode dummy;
    dummy.val = 0;
    dummy.next = head;

    ListNode *fast = head;
    for (int64_t i = 0; i < n; i++) {
        if (fast) fast = fast->next;
    }

    ListNode *slow = &dummy;
    while (fast) {
        fast = fast->next;
        if (slow->next) slow = slow->next;
    }

    if (slow->next) {
        ListNode *target = slow->next;
        slow->next = target->next;
        free(target);
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

int main(void) {
    const int64_t n_values = 100;
    const int64_t k_iters = 500000;

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        ListNode *list = build_list(n_values);
        int64_t n = (k % n_values) + 1;
        ListNode *out = remove_nth_from_end(list, n);
        if (out) sum += out->val;
        chain_free(out);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
