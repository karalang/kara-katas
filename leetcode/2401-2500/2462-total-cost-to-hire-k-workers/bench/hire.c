// LeetCode #2462: Total Cost to Hire K Workers -- the bench, the ★ arm in
// C: two binary min-heaps of `(cost, index)` pairs, the first and the
// last `candidates` workers, each session taking the cheaper top and
// refilling its heap from the untaken middle.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t cost, index;
} Item;

typedef struct {
    Item *items;
    int64_t len;
} Heap;

static int less(Item a, Item b) {
    return a.cost < b.cost || (a.cost == b.cost && a.index < b.index);
}

static void push(Heap *h, Item x) {
    int64_t i = h->len++;
    while (i > 0) {
        int64_t up = (i - 1) / 2;
        if (!less(x, h->items[up])) break;
        h->items[i] = h->items[up];
        i = up;
    }
    h->items[i] = x;
}

static Item pop(Heap *h) {
    Item top = h->items[0];
    Item x = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t c = 2 * i + 1;
        if (c >= h->len) break;
        if (c + 1 < h->len && less(h->items[c + 1], h->items[c])) c++;
        if (!less(h->items[c], x)) break;
        h->items[i] = h->items[c];
        i = c;
    }
    if (h->len > 0) h->items[i] = x;
    return top;
}

static int64_t total_cost(const int64_t *costs, int64_t n, int64_t k, int64_t candidates, Heap *front, Heap *back) {
    front->len = back->len = 0;
    int64_t next = 0, last = n - 1;
    while (next < candidates && next <= last) {
        push(front, (Item){costs[next], next});
        next++;
    }
    while (n - 1 - last < candidates && next <= last) {
        push(back, (Item){costs[last], last});
        last--;
    }
    int64_t total = 0;
    for (int64_t s = 0; s < k; s++) {
        int take_front = front->len > 0 && (back->len == 0 || !less(back->items[0], front->items[0]));
        if (take_front) {
            total += pop(front).cost;
            if (next <= last) {
                push(front, (Item){costs[next], next});
                next++;
            }
        } else {
            total += pop(back).cost;
            if (next <= last) {
                push(back, (Item){costs[last], last});
                last--;
            }
        }
    }
    return total;
}

static int64_t seed = 2462;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

#define LISTS 10
#define N 100000

int main(void) {
    // 10 lists of 10^5 costs from 1 to 10^5 built once; then 32 passes,
    // each setting one cost of every list from the checksum so far, then
    // answering every list with k of 5 10^4 and 1 + 97 p candidates,
    // folding the answer plus the pass into the checksum
    int64_t *lists = malloc(sizeof(int64_t) * LISTS * N);
    for (int64_t i = 0; i < LISTS * N; i++) lists[i] = 1 + wide_random() % 100000;
    Heap front = {malloc(sizeof(Item) * N), 0}, back = {malloc(sizeof(Item) * N), 0};
    int64_t check = 0;
    for (int64_t p = 0; p < 32; p++) {
        int64_t candidates = 1 + 97 * p;
        for (int64_t a = 0; a < LISTS; a++) {
            int64_t *row = lists + a * N;
            row[(check + a) % N] = 1 + check % 100000;
            check = (check * 31 + total_cost(row, N, 50000, candidates, &front, &back) + p) % 1000000007;
        }
    }
    free(front.items);
    free(back.items);
    free(lists);
    printf("32 passes over 10 lists of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
