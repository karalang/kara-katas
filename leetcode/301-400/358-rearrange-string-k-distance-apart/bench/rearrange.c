// Benchmark for #358 -- mirror of rearrange.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t left, neg; } Item;

// Max-heap on (left, neg), lexicographic.
static int less(Item a, Item b) {
    return a.left < b.left || (a.left == b.left && a.neg < b.neg);
}

static void heap_push(Item *h, int *n, Item x) {
    int i = (*n)++;
    h[i] = x;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (!less(h[p], h[i])) break;
        Item t = h[p]; h[p] = h[i]; h[i] = t;
        i = p;
    }
}

static Item heap_pop(Item *h, int *n) {
    Item top = h[0];
    h[0] = h[--(*n)];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < *n && less(h[m], h[l])) m = l;
        if (r < *n && less(h[m], h[r])) m = r;
        if (m == i) break;
        Item t = h[m]; h[m] = h[i]; h[i] = t;
        i = m;
    }
    return top;
}

// Writes the arrangement into out and returns its length (0 if none).
static int64_t rearrange(const char *s, int64_t n, int64_t k, char *out) {
    int64_t counts[26] = {0};
    for (int64_t i = 0; i < n; i++) counts[s[i] - 'a']++;
    Item heap[26];
    int hn = 0;
    for (int c = 0; c < 26; c++)
        if (counts[c] > 0) heap_push(heap, &hn, (Item){counts[c], -c});
    // Ring buffer queue: it never holds more than k + 1 entries.
    int64_t cap = k + 2;
    Item *q = malloc(sizeof(Item) * cap);
    int64_t qh = 0, qlen = 0;
    for (int64_t pos = 0; pos < n; pos++) {
        if (hn == 0) { free(q); return 0; }
        Item it = heap_pop(heap, &hn);
        int64_t c = -it.neg;
        out[pos] = (char)('a' + c);
        q[(qh + qlen) % cap] = (Item){it.left - 1, c};
        qlen++;
        if (qlen >= k) {
            Item f = q[qh];
            qh = (qh + 1) % cap;
            qlen--;
            if (f.left > 0) heap_push(heap, &hn, (Item){f.left, -f.neg});
        }
    }
    free(q);
    return n;
}

int main(void) {
    int64_t seed = 358, possible = 0, checksum = 0;
    char *s = malloc(50000), *r = malloc(50000);
    for (int round = 0; round < 200; round++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t width = (seed / 65536) % 23 + 4;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t k = (seed / 65536) % 8 + 1;
        for (int i = 0; i < 50000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t draw = seed / 65536;
            int64_t c = draw % 8 == 0 ? 0 : (draw / 8) % width;
            s[i] = (char)('a' + c);
        }
        int64_t len = rearrange(s, 50000, k, r);
        if (len == 50000) possible++;
        for (int64_t i = 0; i < len; i++) checksum = (checksum * 31 + r[i]) % 1000000007;
        checksum = (checksum * 31 + 7) % 1000000007;
    }
    printf("%lld of 200 strings can be arranged, checksum %lld\n", (long long)possible, (long long)checksum);
    free(s);
    free(r);
    return 0;
}
