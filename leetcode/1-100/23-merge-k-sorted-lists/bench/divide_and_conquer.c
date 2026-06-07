/*
 * Benchmark workload — Merge k Sorted Lists (LeetCode #23), divide and
 * conquer. C mirror of bench/divide_and_conquer.kara. Plain malloc/free
 * linked list — Kāra's `shared struct` and Rust's `Rc<RefCell<>>` are
 * single-owner in this workload (k lists per iteration, merged then freed
 * at iteration end), so the C mirror expresses the same alloc-per-node
 * build + in-place pairwise re-link + drop shape without RC overhead —
 * the cleanest LLVM-backend floor.
 *
 * Same k/N/K, stride-k interleaving, and full-traversal sink. The merged
 * list is freed after the sink read. See ../README.md § Benchmarks.
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

static ListNode *merge_k_lists(ListNode **lists, int64_t k) {
    if (k == 0) return NULL;
    for (int64_t interval = 1; interval < k; interval *= 2) {
        for (int64_t i = 0; i + interval < k; i += 2 * interval) {
            lists[i] = merge_two_lists(lists[i], lists[i + interval]);
        }
    }
    return lists[0];
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
    const int64_t k_lists = 8;
    const int64_t n_values = 128;
    const int64_t k_iters = 100000;

    int64_t total = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        ListNode *lists[8];
        for (int64_t j = 0; j < k_lists; j++) {
            lists[j] = build_list(j, k_lists, n_values);
        }
        ListNode *merged = merge_k_lists(lists, k_lists);
        total += sum_list(merged);
        chain_free(merged);
    }
    printf("%lld\n", (long long)total);
    return 0;
}
