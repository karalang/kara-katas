/* Benchmark harness for LeetCode #126 — Word Ladder II.
 * Mirrors word_ladder_ii.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so two are hand-rolled: open addressing with linear
 * probing keyed by a fixed-width char[8] (every word here is 5 ASCII bytes).
 * The hash is FxHash with the SAME constants Kara's Map[String, _] uses
 * (h = rotl(h,5) ^ byte; h *= 0x517cc1b727220a95), so this lane is equal-hash
 * by construction.
 *
 * The predecessor map stores a growable array of Words per slot, and the
 * read-modify-write in the BFS COPIES the list out, appends, and writes it
 * back — matching what Kara/Rust/Go's `Map[String, Vec[String]]` update does,
 * rather than appending in place, which would skip work the other four pay.
 *
 * One honest asymmetry, sized in ../README.md: the candidate word is built into
 * an automatic char[8], so C does not allocate per candidate the way the other
 * four do.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WLEN 5
#define NAMELEN 8
#define ALPHA 5
#define TOTAL 3125
#define ITERS 24
#define MAPCAP 8192 /* power of two, > 2x TOTAL */
#define MODV 1000000007LL

typedef char Word[NAMELEN];

typedef struct {
    Word key;
    unsigned char used;
} Slot;

typedef struct {
    Word key;
    unsigned char used;
    Word *list;
    int len;
    int cap;
} PredSlot;

static unsigned long long fx_hash(const char *s) {
    unsigned long long h = 0;
    for (; *s; s++) {
        h = ((h << 5) | (h >> 59)) ^ (unsigned long long)(unsigned char)*s;
        h *= 0x517cc1b727220a95ULL;
    }
    return h;
}

static Slot *slot_for(Slot *m, const char *key) {
    size_t h = (size_t)(fx_hash(key) & (MAPCAP - 1));
    while (m[h].used && strcmp(m[h].key, key) != 0) {
        h = (h + 1) & (MAPCAP - 1);
    }
    return &m[h];
}

static int map_has(Slot *m, const char *key) { return slot_for(m, key)->used; }

static void map_put(Slot *m, const char *key) {
    Slot *s = slot_for(m, key);
    if (!s->used) {
        s->used = 1;
        memcpy(s->key, key, NAMELEN);
    }
}

static PredSlot *pred_slot_for(PredSlot *m, const char *key) {
    size_t h = (size_t)(fx_hash(key) & (MAPCAP - 1));
    while (m[h].used && strcmp(m[h].key, key) != 0) {
        h = (h + 1) & (MAPCAP - 1);
    }
    return &m[h];
}

static char nth_letter(long long n) { return (char)('a' + (n % 26)); }

static Slot word_set[MAPCAP];
static Slot visited[MAPCAP];
static Slot in_next[MAPCAP];
static PredSlot preds[MAPCAP];

static Word cur[TOTAL];
static Word nxt[TOTAL];
static Word path[TOTAL];
static long long npath;

static void preds_clear(void) {
    for (size_t i = 0; i < MAPCAP; i++) {
        if (preds[i].used) {
            free(preds[i].list);
        }
    }
    memset(preds, 0, sizeof(preds));
}

/* Copy the current list out, append `val`, write it back — the copy-back shape
 * the other four mirrors pay through Map[String, Vec[String]]. */
static void preds_append(const char *key, const char *val) {
    PredSlot *s = pred_slot_for(preds, key);
    int oldlen = s->used ? s->len : 0;
    Word *copy = malloc(sizeof(Word) * (size_t)(oldlen + 1));
    for (int i = 0; i < oldlen; i++) {
        memcpy(copy[i], s->list[i], NAMELEN);
    }
    memcpy(copy[oldlen], val, NAMELEN);
    if (s->used) {
        free(s->list);
    } else {
        s->used = 1;
        memcpy(s->key, key, NAMELEN);
    }
    s->list = copy;
    s->len = oldlen + 1;
    s->cap = oldlen + 1;
}

static long long path_digest(void) {
    long long h = 0;
    for (long long idx = npath - 1; idx >= 0; idx--) {
        const char *w = path[idx];
        for (const char *p = w; *p; p++) {
            h = (h * 131 + ((long long)(unsigned char)*p - 96)) % MODV;
        }
        h = (h * 131 + 27) % MODV;
    }
    return h;
}

static void dfs(const char *word, const char *begin, long long *count,
                long long *digest) {
    if (strcmp(word, begin) == 0) {
        *digest = (*digest + path_digest()) % MODV;
        (*count)++;
        return;
    }
    PredSlot *s = pred_slot_for(preds, word);
    if (!s->used) {
        return;
    }
    int n = s->len;
    Word *plist = malloc(sizeof(Word) * (size_t)n);
    memcpy(plist, s->list, sizeof(Word) * (size_t)n);
    for (int i = 0; i < n; i++) {
        memcpy(path[npath++], plist[i], NAMELEN);
        dfs(plist[i], begin, count, digest);
        npath--;
    }
    free(plist);
}

typedef struct {
    long long count;
    long long len;
    long long digest;
} LadderResult;

static LadderResult find_ladders(const char *begin, const char *end,
                                 const Word *words) {
    LadderResult zero = {0, 0, 0};

    memset(word_set, 0, sizeof(word_set));
    for (long long i = 0; i < TOTAL; i++) {
        map_put(word_set, words[i]);
    }
    if (!map_has(word_set, end)) {
        return zero;
    }

    preds_clear();
    memset(visited, 0, sizeof(visited));
    map_put(visited, begin);
    long long ncur = 0;
    memcpy(cur[ncur++], begin, NAMELEN);
    int found = 0;
    long long depth = 1;

    while (ncur > 0 && !found) {
        memset(in_next, 0, sizeof(in_next));
        long long nnxt = 0;
        for (long long i = 0; i < ncur; i++) {
            const char *word = cur[i];
            /* neighbors() */
            long long n = (long long)strlen(word);
            for (long long pos = 0; pos < n; pos++) {
                unsigned char orig = (unsigned char)word[pos];
                for (long long c = 0; c < 26; c++) {
                    if ((c + 97) == (long long)orig) {
                        continue;
                    }
                    Word cand;
                    memcpy(cand, word, NAMELEN);
                    cand[pos] = nth_letter(c);
                    if (!map_has(word_set, cand)) {
                        continue;
                    }
                    if (map_has(visited, cand)) {
                        continue;
                    }
                    preds_append(cand, word);
                    if (!map_has(in_next, cand)) {
                        if (strcmp(cand, end) == 0) {
                            found = 1;
                        }
                        map_put(in_next, cand);
                        memcpy(nxt[nnxt++], cand, NAMELEN);
                    }
                }
            }
        }
        for (long long k = 0; k < nnxt; k++) {
            map_put(visited, nxt[k]);
        }
        memcpy(cur, nxt, sizeof(Word) * (size_t)nnxt);
        ncur = nnxt;
        depth++;
    }

    if (!found) {
        return zero;
    }

    npath = 0;
    memcpy(path[npath++], end, NAMELEN);
    long long count = 0;
    long long digest = 0;
    dfs(end, begin, &count, &digest);

    LadderResult r = {count, depth, digest};
    return r;
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
        LadderResult r = find_ladders(words[b], words[e], words);
        sink = (sink * 1000003 + r.count * 7 + r.len * 13 + r.digest) % MODV;
    }
    printf("%lld\n", sink);
    return 0;
}
