// LeetCode #1048: Longest String Chain -- C mirror of
// bench/longest_chain.kara. C has no map, so the map from word to chain
// length is a chained hash table (FNV-1a over the bytes), allocated afresh
// for each list as the other languages' maps are, with each word copied in
// as its key. Each predecessor is built in a buffer and looked up.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 1048;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct { char *s; int len; } Word;

typedef struct Entry { char *key; int len; long long value; struct Entry *next; } Entry;

static uint64_t fnv(const char *s, int len) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < len; i++) { h ^= (unsigned char)s[i]; h *= 1099511628211ULL; }
    return h;
}

static int by_length(const void *a, const void *b) {
    return ((const Word *)a)->len - ((const Word *)b)->len;
}

static long long longest_str_chain(const Word *words, int n) {
    Word *sorted = malloc(n * sizeof(Word));
    memcpy(sorted, words, n * sizeof(Word));
    qsort(sorted, n, sizeof(Word), by_length);
    int buckets = 1;
    while (buckets < 2 * n) buckets *= 2;
    Entry **head = calloc(buckets, sizeof(Entry *));
    Entry *pool = malloc(n * sizeof(Entry));
    int used = 0;
    long long best = 0;
    char pred[32];
    for (int k = 0; k < n; k++) {
        const Word *w = &sorted[k];
        long long here = 1;
        for (int i = 0; i < w->len; i++) {
            memcpy(pred, w->s, i);
            memcpy(pred + i, w->s + i + 1, w->len - i - 1);
            int plen = w->len - 1;
            for (Entry *e = head[fnv(pred, plen) & (buckets - 1)]; e; e = e->next)
                if (e->len == plen && memcmp(e->key, pred, plen) == 0) {
                    if (e->value + 1 > here) here = e->value + 1;
                    break;
                }
        }
        uint64_t slot = fnv(w->s, w->len) & (buckets - 1);
        Entry *found = NULL;
        for (Entry *e = head[slot]; e; e = e->next)
            if (e->len == w->len && memcmp(e->key, w->s, w->len) == 0) { found = e; break; }
        if (found) {
            found->value = here;
        } else {
            Entry *e = &pool[used++];
            e->key = malloc(w->len);
            memcpy(e->key, w->s, w->len);
            e->len = w->len;
            e->value = here;
            e->next = head[slot];
            head[slot] = e;
        }
        if (here > best) best = here;
    }
    for (int i = 0; i < used; i++) free(pool[i].key);
    free(pool);
    free(head);
    free(sorted);
    return best;
}

int main(void) {
    const int lists = 100, count = 2000, rounds = 5;
    Word **all = malloc(lists * sizeof(Word *));
    for (int l = 0; l < lists; l++) {
        all[l] = malloc(count * sizeof(Word));
        for (int k = 0; k < count; k++) {
            int n = next_random() % 16 + 1;
            all[l][k].s = malloc(n);
            all[l][k].len = n;
            for (int i = 0; i < n; i++) all[l][k].s[i] = 'a' + next_random() % 3;
        }
    }
    long long total = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int l = 0; l < lists; l++) {
            long long answer = longest_str_chain(all[l], count);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    printf("%d lists of %d words, %d rounds: total %lld, checksum %lld\n", lists, count, rounds, total, check);
    return 0;
}
