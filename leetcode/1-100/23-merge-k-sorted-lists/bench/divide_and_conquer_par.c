/* LeetCode #23 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR,
 * merge k sorted lists / divide-and-conquer). Same per-iteration
 * build-k-lists + pairwise-merge + sum-and-free shape as
 * divide_and_conquer.c; the K=100k outer reduction is split across a
 * fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk,
 * join+merge). Raw OS threads, no runtime — the ceiling auto-par is
 * measured against. Sink matches the kara/rust/c/go mirrors.
 * Build: clang -O3 -pthread divide_and_conquer_par.c -o … */
#include <pthread.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

#define K_LISTS 8
#define N_VALUES 128
#define K_ITERS 100000LL

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

typedef struct {
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        ListNode *lists[K_LISTS];
        for (int64_t j = 0; j < K_LISTS; j++) {
            lists[j] = build_list(j, K_LISTS, N_VALUES);
        }
        ListNode *merged = merge_k_lists(lists, K_LISTS);
        s += sum_list(merged);
        chain_free(merged);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].start = (int64_t)w * chunk;
        works[w].end = (w == nworkers - 1) ? K_ITERS : ((int64_t)w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    int64_t total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%lld\n", (long long)total);
    free(threads);
    free(works);
    return 0;
}
