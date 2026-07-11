/*
 * Benchmark workload — Remove Duplicates from Sorted List (LeetCode #83).
 * C mirror of bench/remove_duplicates_list.kara. Plain malloc/free singly-linked list
 * — single-owner in this workload, the honest metal floor against Kāra's
 * `shared struct` and Rust's `Rc<RefCell<>>`. Each iteration builds a fresh list
 * (M=300, every value duplicated), runs the keep-one dedup (freeing spliced nodes),
 * folds the survivors through a rolling polynomial hash, then frees the rest.
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

static ListNode *delete_duplicates(ListNode *head) {
    ListNode *cur = head;
    while (cur != NULL) {
        if (cur->next != NULL) {
            if (cur->val == cur->next->val) {
                ListNode *dup = cur->next;
                cur->next = dup->next;
                free(dup);              /* single-owner: reclaim the spliced node */
            } else {
                cur = cur->next;
            }
        } else {
            break;
        }
    }
    return head;
}

static ListNode *build(int64_t m, int64_t dup) {
    ListNode dummy;
    dummy.next = NULL;
    ListNode *tail = &dummy;
    for (int64_t v = 0; v < m; v++) {
        for (int64_t d = 0; d < dup; d++) {
            ListNode *node = node_new(v);
            tail->next = node;
            tail = node;
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
    const int64_t m = 300, dup = 2, total = 70000, modulus = 1000000007;
    int64_t sum = 0;
    for (int64_t k = 0; k < total; k++) {
        ListNode *list = build(m, dup);
        ListNode *dd = delete_duplicates(list);
        sum = (sum * 131 + fold_and_free(dd, k)) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
