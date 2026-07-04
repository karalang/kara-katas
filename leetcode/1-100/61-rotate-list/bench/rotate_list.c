/*
 * Benchmark workload — Rotate List (LeetCode #61).
 * C mirror of bench/rotate_list.kara. Plain malloc/free linked list — Kāra's
 * `shared struct` and Rust's `Rc<RefCell<>>` are single-owner in this workload
 * (one list per iteration, dropped at iteration end), so the C mirror expresses
 * the same alloc-per-node build + close-the-ring + cut shape without RC
 * overhead — the cleanest LLVM-backend floor.
 *
 * Same N/K, append list-builder, rotation sweep `r = k % (2*N)`, and sink.
 * The caller frees the whole (now-linear) chain after the sink read; there is
 * no per-node free inside rotate — rotation only re-links, it deletes nothing.
 * See ../README.md § Benchmarks.
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

static ListNode *rotate_right(ListNode *head, int64_t k) {
    int64_t len = 0;
    ListNode *cur = head;
    ListNode *tail = NULL;
    while (cur) {
        len++;
        tail = cur;
        cur = cur->next;
    }

    if (len == 0) return NULL;
    int64_t shift = k % len;
    if (shift == 0) return head;

    tail->next = head; /* close the ring */

    int64_t steps = len - shift - 1;
    ListNode *new_tail = head;
    for (int64_t i = 0; i < steps; i++) {
        if (new_tail) new_tail = new_tail->next;
    }

    ListNode *result = head;
    if (new_tail) {
        result = new_tail->next;
        new_tail->next = NULL; /* sever the ring */
    }
    return result;
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
    const int64_t span = 200; /* 2*N */
    const int64_t k_iters = 500000;

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        ListNode *list = build_list(n_values);
        int64_t r = k % span;
        ListNode *out = rotate_right(list, r);
        if (out) sum += out->val;
        chain_free(out);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
