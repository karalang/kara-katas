// Benchmark: LeetCode #1090 Largest Values From Labels -- C mirror of the ★
// arm: (value, label) pairs sorted by value from the largest (`qsort`, C's
// library sort), taken while their label has uses left (an
// open-addressing hash map of uses per label, built per call as Kāra's `Map`
// is). Same workload and sink as largest_values_from_labels.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PROBLEMS 100
#define LEN 20000

typedef struct {
    int64_t value, label;
} Item;

// Larger value first. `qsort` is not stable, which the answer does not need:
// items of equal value are interchangeable to the greedy.
static int by_value_down(const void *x, const void *y) {
    int64_t a = ((const Item *)x)->value, b = ((const Item *)y)->value;
    return (b > a) - (b < a);
}

typedef struct {
    int64_t *keys, *vals;
    uint8_t *full;
    uint64_t mask;
} Map;

static uint64_t mix(uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

static int64_t *map_slot(Map *m, int64_t key) {
    uint64_t i = mix((uint64_t)key) & m->mask;
    while (m->full[i] && m->keys[i] != key) {
        i = (i + 1) & m->mask;
    }
    if (!m->full[i]) {
        m->full[i] = 1;
        m->keys[i] = key;
        m->vals[i] = 0;
    }
    return &m->vals[i];
}

static int64_t largest_vals_from_labels(const int64_t *values, const int64_t *labels, int64_t n,
                                        int64_t num_wanted, int64_t use_limit) {
    Item *items = malloc(n * sizeof(Item));
    for (int64_t i = 0; i < n; i++) {
        items[i].value = values[i];
        items[i].label = labels[i];
    }
    qsort(items, n, sizeof(Item), by_value_down);
    uint64_t cap = 16;
    while (cap < 2 * (uint64_t)n) {
        cap *= 2;
    }
    Map used = {malloc(cap * 8), malloc(cap * 8), calloc(cap, 1), cap - 1};
    int64_t taken = 0, sum = 0;
    for (int64_t i = 0; i < n; i++) {
        if (taken == num_wanted) {
            break;
        }
        int64_t *uses = map_slot(&used, items[i].label);
        if (*uses < use_limit) {
            *uses += 1;
            sum += items[i].value;
            taken++;
        }
    }
    free(used.keys);
    free(used.vals);
    free(used.full);
    free(items);
    return sum;
}

static int64_t seed = 1090;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *values[PROBLEMS], *labels[PROBLEMS];
    for (int k = 0; k < PROBLEMS; k++) {
        values[k] = malloc(LEN * sizeof(int64_t));
        labels[k] = malloc(LEN * sizeof(int64_t));
        for (int i = 0; i < LEN; i++) {
            values[k][i] = next_random() % 20001;
            labels[k][i] = next_random() % 1000;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int64_t k = 0; k < PROBLEMS; k++) {
            int64_t num_wanted = (round * 7919 + k * 31) % 20000 + 1;
            int64_t use_limit = (round * 13 + k) % 20 + 1;
            int64_t answer = largest_vals_from_labels(values[k], labels[k], LEN, num_wanted, use_limit);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("20 rounds over 100 problems of 2 * 10^4 items: answers sum to %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int k = 0; k < PROBLEMS; k++) {
        free(values[k]);
        free(labels[k]);
    }
    return 0;
}
