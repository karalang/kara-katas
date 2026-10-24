// Benchmark: LeetCode #950 Reveal Cards In Increasing Order -- the ★ arm,
// the reveals played on the places, on decks of 1000 cards, LeetCode's
// largest. Mirrors deck_revealed_increasing.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000
#define COUNT 20

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// the places in a ring buffer of n slots, a queue from head to tail
static int64_t *deck_revealed_increasing(const int64_t *deck, int64_t n) {
    int64_t *sorted = malloc(sizeof(int64_t) * (size_t)n);
    memcpy(sorted, deck, sizeof(int64_t) * (size_t)n);
    qsort(sorted, (size_t)n, sizeof(int64_t), cmp_i64);
    int64_t *places = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) places[i] = i;
    int64_t head = 0, len = n;
    int64_t *out = calloc((size_t)n, sizeof(int64_t));
    for (int64_t k = 0; k < n; k++) {
        int64_t place = places[head];
        head = (head + 1) % n;
        len--;
        out[place] = sorted[k];
        if (len > 0) {
            int64_t next = places[head];
            head = (head + 1) % n;
            places[(head + len - 1) % n] = next;
        }
    }
    free(places);
    free(sorted);
    return out;
}

static int64_t seed = 950;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t decks[COUNT][N];

int main(void) {
    const int64_t rounds = 1000, count = COUNT, n = N;
    static unsigned char taken[1000001];
    for (int64_t c = 0; c < count; c++) {
        memset(taken, 0, sizeof taken);
        int64_t len = 0;
        while (len < n) {
            int64_t a = next_random();
            int64_t b = next_random();
            int64_t v = 1 + (a * 32768 + b) % 1000000;
            if (!taken[v]) {
                taken[v] = 1;
                decks[c][len++] = v;
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t *out = deck_revealed_increasing(decks[(r + i) % count], n);
            total += out[n - 1];
            check = (check * 1000003 + out[(r * 7 + i) % n]) % 1000000007;
            free(out);
        }
    }
    printf("%lld rounds over %lld decks of %lld cards: last cards adding to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    return 0;
}
