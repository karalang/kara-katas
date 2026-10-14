/*
 * LeetCode 632 -- Smallest Range Covering Elements from K Lists, bench
 * mirror in C.
 *
 * The ★ arm of smallest_range.kara: one value from each list in a
 * smallest-first binary heap of (value, list, index) triples, compared
 * in that order, with the largest held value tracked beside it. Same
 * 10 inputs, same rounds, same output line. The lists are kept as one
 * malloc'd array each, sorted with qsort.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t value, list, at;
} Entry;

static int less(const Entry *a, const Entry *b) {
    if (a->value != b->value) return a->value < b->value;
    if (a->list != b->list) return a->list < b->list;
    return a->at < b->at;
}

typedef struct {
    Entry *items;
    int64_t len, cap;
} Heap;

static void heap_push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 4;
        h->items = realloc(h->items, h->cap * sizeof(Entry));
    }
    int64_t i = h->len++;
    while (i > 0) {
        int64_t parent = (i - 1) / 2;
        if (!less(&e, &h->items[parent])) break;
        h->items[i] = h->items[parent];
        i = parent;
    }
    h->items[i] = e;
}

static Entry heap_pop(Heap *h) {
    Entry top = h->items[0];
    Entry last = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t child = 2 * i + 1;
        if (child >= h->len) break;
        if (child + 1 < h->len && less(&h->items[child + 1], &h->items[child])) child++;
        if (!less(&h->items[child], &last)) break;
        h->items[i] = h->items[child];
        i = child;
    }
    if (h->len > 0) h->items[i] = last;
    return top;
}

typedef struct {
    int64_t *values;
    int64_t len;
} List;

static void smallest_range(const List *nums, int64_t k, int64_t *out_low, int64_t *out_high) {
    Heap queue = {0};
    int64_t high = nums[0].values[0];
    for (int64_t list = 0; list < k; list++) {
        heap_push(&queue, (Entry){nums[list].values[0], list, 0});
        if (nums[list].values[0] > high) high = nums[list].values[0];
    }
    int64_t best_low = 0, best_high = 0;
    int found = 0;
    for (;;) {
        Entry e = heap_pop(&queue);
        if (!found || high - e.value < best_high - best_low) {
            best_low = e.value;
            best_high = high;
            found = 1;
        }
        if (e.at + 1 == nums[e.list].len) break;
        int64_t next = nums[e.list].values[e.at + 1];
        if (next > high) high = next;
        heap_push(&queue, (Entry){next, e.list, e.at + 1});
    }
    free(queue.items);
    *out_low = best_low;
    *out_high = best_high;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int compare(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static List *random_lists(int64_t count, int64_t length, int64_t *seed) {
    List *nums = malloc(count * sizeof(List));
    for (int64_t i = 0; i < count; i++) {
        nums[i].values = malloc(length * sizeof(int64_t));
        nums[i].len = length;
        for (int64_t j = 0; j < length; j++) {
            int64_t wide = next_random(seed) * 32768;
            wide += next_random(seed);
            nums[i].values[j] = wide % 200001 - 100000;
        }
        qsort(nums[i].values, length, sizeof(int64_t), compare);
    }
    return nums;
}

int main(void) {
    int64_t seed = 632;
    List *inputs[10];
    for (int i = 0; i < 10; i++) inputs[i] = random_lists(3500, 50, &seed);
    const int64_t rounds = 30;
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t low, high;
        smallest_range(inputs[round % 10], 3500, &low, &high);
        total += high - low;
        checksum = (checksum * 31 + low * 101 + high + 100000000) % 1000000007;
    }
    printf("10 inputs of 3500 lists, %lld rounds: total width %lld, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)checksum);
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 3500; j++) free(inputs[i][j].values);
        free(inputs[i]);
    }
    return 0;
}
