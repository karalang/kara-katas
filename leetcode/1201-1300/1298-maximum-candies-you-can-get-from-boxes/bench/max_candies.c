// LeetCode #1298 bench: the ★ arm (a breadth-first walk over the boxes that
// can be opened, each queued once, when it is both held and open) over 100
// cases of 1000 boxes, built once; then 5000 passes, each flipping one box of
// every case between open and locked, chosen from the checksum so far,
// answering it, and folding the answer into the checksum. Each box is queued
// at most once, so the queue is an array of n read from a moving head; the
// lists of keys and boxes inside are arrays that grow by doubling.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, sizeof(int64_t) * l->cap);
    }
    l->items[l->len++] = x;
}

static int64_t max_candies(int64_t n, const int64_t *status, const int64_t *candies, const List *keys,
                           const List *contained_boxes, const List *initial_boxes) {
    char *open = malloc(n), *held = calloc(n, 1), *queued = calloc(n, 1);
    int64_t *queue = malloc(sizeof(int64_t) * n);
    int64_t head = 0, tail = 0;
    for (int64_t i = 0; i < n; i++) open[i] = status[i] == 1;
    for (int64_t i = 0; i < initial_boxes->len; i++) {
        int64_t b = initial_boxes->items[i];
        held[b] = 1;
        if (open[b] && !queued[b]) {
            queued[b] = 1;
            queue[tail++] = b;
        }
    }
    int64_t total = 0;
    while (head < tail) {
        int64_t b = queue[head++];
        total += candies[b];
        for (int64_t i = 0; i < keys[b].len; i++) {
            int64_t k = keys[b].items[i];
            open[k] = 1;
            if (held[k] && !queued[k]) {
                queued[k] = 1;
                queue[tail++] = k;
            }
        }
        for (int64_t i = 0; i < contained_boxes[b].len; i++) {
            int64_t c = contained_boxes[b].items[i];
            held[c] = 1;
            if (open[c] && !queued[c]) {
                queued[c] = 1;
                queue[tail++] = c;
            }
        }
    }
    free(open);
    free(held);
    free(queued);
    free(queue);
    return total;
}

static int64_t seed = 1298;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    int64_t n;
    int64_t *status, *candies;
    List *keys, *contained;
    List initial;
} Case;

static int contains(const List *l, int64_t x) {
    for (int64_t i = 0; i < l->len; i++)
        if (l->items[i] == x) return 1;
    return 0;
}

static Case make_case(int64_t n, int64_t open, int64_t initial_in, int64_t nest, int64_t max_keys) {
    int64_t *order = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) order[i] = i;
    for (int64_t i = 0; i < n; i++) {
        int64_t j = i + next_random() % (n - i);
        int64_t t = order[i];
        order[i] = order[j];
        order[j] = t;
    }
    Case c = {n, calloc(n, sizeof(int64_t)), calloc(n, sizeof(int64_t)), calloc(n, sizeof(List)),
              calloc(n, sizeof(List)), {0}};
    for (int64_t i = 0; i < n; i++) {
        int64_t b = order[i];
        int64_t roll = next_random() % 100;
        if (i > 0 && roll < nest) {
            int64_t parent = order[next_random() % i];
            push(&c.contained[parent], b);
        } else if (next_random() % 100 < initial_in) {
            push(&c.initial, b);
        }
        if (next_random() % 100 < open) c.status[b] = 1;
        c.candies[b] = 1 + next_random() % 1000;
        int64_t count = next_random() % (max_keys + 1);
        for (int64_t j = 0; j < count; j++) {
            int64_t k = next_random() % n;
            if (!contains(&c.keys[b], k)) push(&c.keys[b], k);
        }
    }
    free(order);
    return c;
}

int main(void) {
    Case cases[100];
    for (int64_t t = 0; t < 100; t++) cases[t] = make_case(1000, 10 + t % 40, 5 + t % 20, 60 + t % 40, 1 + t % 4);
    int64_t check = 0;
    for (int64_t p = 0; p < 5000; p++) {
        for (int64_t t = 0; t < 100; t++) {
            Case *c = &cases[t];
            int64_t b = check % 1000;
            c->status[b] = 1 - c->status[b];
            int64_t got = max_candies(c->n, c->status, c->candies, c->keys, c->contained, &c->initial);
            check = (check * 31 + got + p) % 1000000007;
        }
    }
    printf("5000 passes over 100 cases of 1000 boxes: checksum %lld\n", (long long)check);
    return 0;
}
