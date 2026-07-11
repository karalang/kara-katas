/*
 * LeetCode #86 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 * Same batch of K=170000 independent partitions as partition_list.c; the associative
 * sum reduction is split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn
 * once, chunk the seed range, join + merge). Raw OS threads, no runtime — the ceiling
 * Kara's auto-par is measured against. This is an allocation-bound workload (fresh
 * M-node list per iteration), so even raw pthreads scale sublinearly (malloc contends).
 * Sink matches the seq mirrors. Build: clang -O3 partition_list_par.c -o … -lpthread
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define M 200
#define ITERS 170000

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

static ListNode *build(int64_t seed) {
    ListNode dummy;
    dummy.next = NULL;
    ListNode *tail = &dummy;
    for (int64_t j = 0; j < M; j++) {
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

static int64_t one(int64_t k) {
    return fold_and_free(partition(build(k), 50), k);
}

typedef struct { int64_t start, end, partial; } Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (int64_t i = w->start; i < w->end; i++)
        s += one(i);
    w->partial = s;
    return NULL;
}

int main(void) {
    int64_t nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) nworkers = 1;
    if (nworkers > ITERS) nworkers = ITERS;

    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = ITERS / nworkers;
    for (int64_t w = 0; w < nworkers; w++) {
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? ITERS : (w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    int64_t total = 0;
    for (int64_t w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%lld\n", (long long)total);
    free(threads);
    free(works);
    return 0;
}
