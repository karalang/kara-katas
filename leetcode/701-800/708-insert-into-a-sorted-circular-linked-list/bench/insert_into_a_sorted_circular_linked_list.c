// LeetCode #708: Insert into a Sorted Circular Linked List -- an arena.
// Benchmark mirror of the Kara star arm: values and next links in two
// growable arrays; walk from the given node to the first gap that fits.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *vals;
    int64_t *next;
    int64_t len;
    int64_t cap;
} Ring;

static void push(Ring *r, int64_t val, int64_t next) {
    if (r->len == r->cap) {
        r->cap = r->cap ? r->cap * 2 : 16;
        r->vals = realloc(r->vals, r->cap * sizeof(int64_t));
        r->next = realloc(r->next, r->cap * sizeof(int64_t));
    }
    r->vals[r->len] = val;
    r->next[r->len] = next;
    r->len += 1;
}

static int fits(int64_t a, int64_t b, int64_t x) {
    if (a <= b) {
        return a <= x && x <= b;
    }
    return x >= a || x <= b;
}

static int64_t insert(Ring *r, int64_t head, int64_t insert_val) {
    int64_t id = r->len;
    if (head < 0) {
        push(r, insert_val, id);
        return id;
    }
    int64_t prev = head;
    for (;;) {
        int64_t curr = r->next[prev];
        if (fits(r->vals[prev], r->vals[curr], insert_val)) {
            break;
        }
        prev = curr;
        if (prev == head) {
            break;
        }
    }
    push(r, insert_val, r->next[prev]);
    r->next[prev] = id;
    return head;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int64_t seed = 708;
    int64_t checksum = 0;
    int64_t n = 20000;
    int64_t *sorted = malloc(n * sizeof(int64_t));
    for (int round = 0; round < 5; round++) {
        for (int ring_no = 0; ring_no < 10; ring_no++) {
            for (int64_t i = 0; i < n; i++) {
                int64_t hi = next_random(&seed);
                int64_t lo = next_random(&seed);
                sorted[i] = (hi * 32768 + lo) % 2000001 - 1000000;
            }
            qsort(sorted, n, sizeof(int64_t), cmp);
            int64_t start = next_random(&seed) % n;
            Ring ring = {NULL, NULL, 0, 0};
            for (int64_t i = 0; i < n; i++) {
                push(&ring, sorted[(start + i) % n], (i + 1) % n);
            }
            int64_t head = 0;
            for (int i = 0; i < 1000; i++) {
                int64_t hi = next_random(&seed);
                int64_t lo = next_random(&seed);
                head = insert(&ring, head, (hi * 32768 + lo) % 2000001 - 1000000);
            }
            int64_t at = head;
            do {
                checksum = (checksum * 31 + ring.vals[at] + 1000001) % 1000000007;
                at = ring.next[at];
            } while (at != head);
            free(ring.vals);
            free(ring.next);
        }
    }
    free(sorted);
    printf("5 rounds of 10 rings of 20000 values, 1000 inserts each: checksum %lld\n",
           (long long)checksum);
    return 0;
}
