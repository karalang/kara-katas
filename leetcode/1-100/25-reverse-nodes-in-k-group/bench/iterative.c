/*
 * Benchmark workload — Reverse Nodes in k-Group (LeetCode #25), iterative.
 * C mirror of bench/iterative.kara. Plain malloc/free linked list — Kāra's
 * `shared struct` and Rust's `Rc<RefCell<>>` are single-owner in this workload
 * (one list per iteration, reversed then freed at iteration end), so the C
 * mirror expresses the same alloc-per-node build + in-place group reversal +
 * drop shape without RC overhead — the cleanest LLVM-backend floor.
 *
 * Same N/K/k and full-traversal sink. The reversed list is freed after the
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

static ListNode *reverse_k_group(ListNode *head, int64_t k) {
    ListNode dummy;
    dummy.val = 0;
    dummy.next = head;
    ListNode *group_prev = &dummy;
    for (;;) {
        /* Probe k nodes ahead; a partial trailing group stays in place. */
        ListNode *probe = group_prev->next;
        int64_t count = 0;
        while (count < k && probe) {
            probe = probe->next;
            count++;
        }
        if (count < k) break;
        ListNode *group_head = group_prev->next;
        /* Reverse exactly k nodes, prev seeded with the suffix. */
        ListNode *prev = probe;
        ListNode *cur = group_prev->next;
        for (int64_t j = 0; j < k; j++) {
            ListNode *nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        group_prev->next = prev;
        group_prev = group_head;
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
        ListNode *reversed = reverse_k_group(list, 5);
        total += sum_list(reversed);
        chain_free(reversed);
    }
    printf("%lld\n", (long long)total);
    return 0;
}
