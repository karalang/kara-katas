/* Benchmark harness for LeetCode #127 — Word Ladder.
 * Mirrors word_ladder.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so one is hand-rolled: open addressing with linear
 * probing, keyed by a fixed-width char[8] (every word here is 5 ASCII bytes).
 * The hash is FxHash with the SAME constants Kara's Map[String, _] uses
 * (h = rotl(h,5) ^ byte; h *= 0x517cc1b727220a95), so this lane is equal-hash
 * by construction rather than by accident.
 *
 * One honest asymmetry: the candidate word is built into an automatic char[8],
 * so C does NOT allocate per candidate the way Kara/Rust/Go's String does.
 * That is the natural way to write it in C, and ../README.md sizes the
 * difference with a malloc-per-candidate discriminator rather than hiding it.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WLEN 5
#define NAMELEN 8
#define ALPHA 5
#define TOTAL 3125
#define ITERS 17

/* The word set and visited set are shaped to match the runtime's Set[T] rather
 * than presized to the workload: heap-allocated per call (like the kata's
 * `Set.new()`) and freed after, capacity 16 initially, power of two, linear
 * probing, doubling with a full rehash when (len + 1) * 4 > capacity * 3 --
 * the runtime map's 75% load factor, which Set[T] shares because it lowers to
 * a Map with a zero-width value. The previous fixed 8192-entry static tables
 * were presized past the 3125-word working set and merely memset, so they
 * never allocated, grew, or rehashed, while the kata's sets climb
 * 16 -> 32 -> ... -> 8192. Presizing to the answer is not a C advantage, it is
 * a different program. */
#define INITIAL_CAPACITY 16UL

typedef char Word[NAMELEN];

typedef struct {
    Word key;
    unsigned char used;
} Slot;

typedef struct {
    Slot *slots;
    size_t cap;
    size_t len;
} Set;

static unsigned long long fx_hash(const char *s) {
    unsigned long long h = 0;
    for (; *s; s++) {
        h = ((h << 5) | (h >> 59)) ^ (unsigned long long)(unsigned char)*s;
        h *= 0x517cc1b727220a95ULL;
    }
    return h;
}

static void map_init(Set *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->slots = (Slot *)calloc(m->cap, sizeof(Slot));
}

static void map_free(Set *m) {
    free(m->slots);
    m->slots = NULL;
}

static Slot *slot_for(Set *m, const char *key) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)(fx_hash(key) & mask);
    while (m->slots[h].used && strcmp(m->slots[h].key, key) != 0) {
        h = (h + 1) & mask;
    }
    return &m->slots[h];
}

static int map_has(Set *m, const char *key) {
    return slot_for(m, key)->used;
}

static void map_grow(Set *m) {
    Slot *old = m->slots;
    size_t ocap = m->cap;

    m->cap = ocap * 2;
    m->slots = (Slot *)calloc(m->cap, sizeof(Slot));

    for (size_t i = 0; i < ocap; i++) {
        if (old[i].used) {
            Slot *s = slot_for(m, old[i].key);
            s->used = 1;
            memcpy(s->key, old[i].key, NAMELEN);
        }
    }
    free(old);
}

static void map_put(Set *m, const char *key) {
    Slot *s = slot_for(m, key);
    if (s->used) {
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
        s = slot_for(m, key);
    }
    s->used = 1;
    memcpy(s->key, key, NAMELEN);
    m->len++;
}

static char nth_letter(long long n) {
    return (char)('a' + (n % 26));
}

static Set word_set;
static Set visited;
static Word cur[TOTAL];
static Word nxt[TOTAL];
static Word nbs[WLEN * 26];

static long long ladder_length(const char *begin, const char *end,
                               const Word *words) {
    map_init(&word_set);
    for (long long i = 0; i < TOTAL; i++) {
        map_put(&word_set, words[i]);
    }
    if (!map_has(&word_set, end)) {
        map_free(&word_set);
        return 0;
    }

    map_init(&visited);
    map_put(&visited, begin);
    long long ncur = 0;
    memcpy(cur[ncur++], begin, NAMELEN);
    long long steps = 1;

    while (ncur > 0) {
        long long nnxt = 0;
        for (long long i = 0; i < ncur; i++) {
            const char *word = cur[i];
            if (strcmp(word, end) == 0) {
                map_free(&visited);
                map_free(&word_set);
                return steps;
            }
            /* neighbors() */
            long long nnb = 0;
            long long n = (long long)strlen(word);
            for (long long pos = 0; pos < n; pos++) {
                unsigned char orig = (unsigned char)word[pos];
                for (long long c = 0; c < 26; c++) {
                    if ((c + 97) != (long long)orig) {
                        Word cand;
                        memcpy(cand, word, NAMELEN);
                        cand[pos] = nth_letter(c);
                        if (map_has(&word_set, cand)) {
                            memcpy(nbs[nnb++], cand, NAMELEN);
                        }
                    }
                }
            }
            for (long long j = 0; j < nnb; j++) {
                if (!map_has(&visited, nbs[j])) {
                    map_put(&visited, nbs[j]);
                    memcpy(nxt[nnxt++], nbs[j], NAMELEN);
                }
            }
        }
        memcpy(cur, nxt, sizeof(Word) * (size_t)nnxt);
        ncur = nnxt;
        steps++;
    }
    map_free(&visited);
    map_free(&word_set);
    return 0;
}

int main(void) {
    static Word words[TOTAL];

    for (long long idx = 0; idx < TOTAL; idx++) {
        long long rem = idx;
        long long div = 625;
        for (long long d = 0; d < WLEN; d++) {
            long long digit = rem / div;
            words[idx][d] = nth_letter(digit);
            rem -= digit * div;
            div /= ALPHA;
        }
        words[idx][WLEN] = '\0';
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long b = (it * 257) % TOTAL;
        long long e = (it * 613 + 1234) % TOTAL;
        long long r = ladder_length(words[b], words[e], words);
        sink = (sink * 31 + r) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}
