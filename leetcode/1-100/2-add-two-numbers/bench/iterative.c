/*
 * LeetCode #2 — iterative add_two_numbers, bench mirror in C.
 *
 * Algorithmic mirror of bench/iterative.{kara,rs}. Same N=100 nine-digit
 * lists built once, K=500_000 iterations. Stdout sink: 8 * K = 4_000_000
 * (999..9 + 999..9 = 1999..98 in reverse-digit storage; first digit is 8).
 *
 * C has no Rc — and Kāra's `shared struct` / Rust's `Rc<RefCell<>>` are
 * single-owner here in practice (each `add_two_numbers` result has one
 * owner: the caller's `out` slot, dropped at end of iteration). So the
 * C mirror uses plain `malloc`/`free` with manual chain drop after the
 * sink read. The codegen-calibration value is the cleanest expression of
 * the same alloc-per-digit + walk-and-drop shape without RC overhead.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *node_new(int64_t val, ListNode *next) {
    ListNode *p = (ListNode *)malloc(sizeof(ListNode));
    p->val = val;
    p->next = next;
    return p;
}

static void chain_free(ListNode *head) {
    while (head) {
        ListNode *next = head->next;
        free(head);
        head = next;
    }
}

static ListNode *add_two_numbers(const ListNode *a, const ListNode *b) {
    ListNode dummy;
    dummy.val = 0;
    dummy.next = NULL;
    ListNode *tail = &dummy;
    int64_t carry = 0;
    while (a || b || carry) {
        int64_t s = carry;
        if (a) { s += a->val; a = a->next; }
        if (b) { s += b->val; b = b->next; }
        ListNode *node = node_new(s % 10, NULL);
        tail->next = node;
        tail = node;
        carry = s / 10;
    }
    return dummy.next;
}

static ListNode *from_array(const int64_t *arr, size_t n) {
    if (n == 0) return NULL;
    ListNode *head = node_new(arr[0], NULL);
    ListNode *tail = head;
    for (size_t i = 1; i < n; i++) {
        ListNode *node = node_new(arr[i], NULL);
        tail->next = node;
        tail = node;
    }
    return head;
}

int main(void) {
    const size_t N = 100;
    const int64_t K = 500000;
    int64_t a[100], b[100];
    for (size_t i = 0; i < N; i++) { a[i] = 9; b[i] = 9; }
    ListNode *l1 = from_array(a, N);
    ListNode *l2 = from_array(b, N);

    int64_t sum = 0;
    for (int64_t k = 0; k < K; k++) {
        ListNode *out = add_two_numbers(l1, l2);
        if (out) sum += out->val;
        chain_free(out);
    }
    printf("%lld\n", (long long)sum);

    chain_free(l1);
    chain_free(l2);
    return 0;
}
