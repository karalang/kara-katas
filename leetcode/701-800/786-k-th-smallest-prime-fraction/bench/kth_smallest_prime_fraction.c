// LeetCode 786 — K-th Smallest Prime Fraction: the bench, in C.
// Mirrors kth_smallest_prime_fraction.kara: a binary heap of the next
// fraction for each denominator, over the same 64 arrays.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t i, j, num, den;
} Fraction;

static int less(const Fraction *a, const Fraction *b) { return a->num * b->den < b->num * a->den; }

typedef struct {
    Fraction *items;
    int64_t len, cap;
} Heap;

static void heap_push(Heap *h, Fraction f) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 4;
        h->items = realloc(h->items, h->cap * sizeof *h->items);
    }
    int64_t at = h->len++;
    while (at > 0) {
        int64_t up = (at - 1) / 2;
        if (!less(&f, &h->items[up])) break;
        h->items[at] = h->items[up];
        at = up;
    }
    h->items[at] = f;
}

static Fraction heap_pop(Heap *h) {
    Fraction top = h->items[0];
    Fraction last = h->items[--h->len];
    int64_t at = 0;
    for (;;) {
        int64_t child = 2 * at + 1;
        if (child >= h->len) break;
        if (child + 1 < h->len && less(&h->items[child + 1], &h->items[child])) child++;
        if (!less(&h->items[child], &last)) break;
        h->items[at] = h->items[child];
        at = child;
    }
    if (h->len > 0) h->items[at] = last;
    return top;
}

static void kth_smallest_prime_fraction(const int64_t *arr, int64_t n, int64_t k, int64_t out[2]) {
    Heap heap = {0};
    for (int64_t j = 1; j < n; j++) heap_push(&heap, (Fraction){0, j, arr[0], arr[j]});
    for (int64_t t = 0; t < k - 1; t++) {
        Fraction f = heap_pop(&heap);
        if (f.i + 1 < f.j) heap_push(&heap, (Fraction){f.i + 1, f.j, arr[f.i + 1], f.den});
    }
    Fraction f = heap_pop(&heap);
    out[0] = f.num;
    out[1] = f.den;
    free(heap.items);
}

static int64_t seed = 786;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char composite[30000];
    static int64_t primes[30000];
    int64_t count_primes = 0;
    for (int64_t p = 2; p < 30000; p++) {
        if (!composite[p]) {
            primes[count_primes++] = p;
            for (int64_t m = p * p; m < 30000; m += p) composite[m] = 1;
        }
    }
    static int64_t arrays[64][1000];
    for (int t = 0; t < 64; t++) {
        static char taken[30000];
        for (int64_t i = 0; i < count_primes; i++) taken[i] = 0;
        int64_t count = 0;
        while (count < 999) {
            int64_t at = next_random() % count_primes;
            if (!taken[at]) {
                taken[at] = 1;
                count++;
            }
        }
        int64_t len = 0;
        arrays[t][len++] = 1;
        for (int64_t at = 0; at < count_primes; at++)
            if (taken[at]) arrays[t][len++] = primes[at];
    }
    const int64_t rounds = 64;
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t hi = next_random();
        int64_t k = 1 + (hi * 32768 + next_random()) % 499500;
        int64_t answer[2];
        kth_smallest_prime_fraction(arrays[r % 64], 1000, k, answer);
        sum += answer[0] + answer[1];
        check = (check * 31 + answer[0] * 7 + answer[1]) % 1000000007;
    }
    printf("%lld rounds of 1000-number arrays: terms sum to %lld, checksum %lld\n",
           (long long)rounds, (long long)sum, (long long)check);
    return 0;
}
