/* Benchmark harness for LeetCode #290 — Word Pattern.
 * Mirrors word_pattern.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so both directions of the bijection are hand-rolled
 * as open-addressing tables (linear probing; FNV-1a + strcmp for the
 * word-keyed one, identity-mixed for the letter-keyed one). Unlike #291 these
 * tables are insert-only within a call — Word Pattern never deletes — so there
 * are no tombstones and no probe-chain growth.
 *
 * Deliberately avoids the two traps that made #291's first C mirror 3.1x too
 * slow: string copies use memcpy (not snprintf), and lengths are computed once
 * rather than per call.
 */

#include <stdio.h>
#include <string.h>

#define NP 8
#define PL 1000
#define ALPHA_N 26
#define ITERS 2500

#define MAXWORD 8
#define SUBLEN (PL * (MAXWORD + 1) + 4)
#define WCAP 4096 /* power of two; > 2x the PL distinct words */

typedef char Word[MAXWORD];

/* letter code -> word */
typedef struct {
    Word val[128];
    unsigned char used[128];
} P2W;

/* word -> letter code */
typedef struct {
    Word key[WCAP];
    long long val[WCAP];
    unsigned char used[WCAP];
} W2P;

static size_t hash_word(const char *s) {
    size_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h ^= (unsigned char)*s;
        h *= 1099511628211ULL;
    }
    return h & (WCAP - 1);
}

static size_t w2p_slot(const W2P *t, const char *key) {
    size_t h = hash_word(key);
    while (t->used[h] && strcmp(t->key[h], key) != 0) {
        h = (h + 1) & (WCAP - 1);
    }
    return h;
}

static char words[PL][MAXWORD];
static int nwords;

static void split_words(const char *s, size_t slen) {
    nwords = 0;
    size_t cur = 0;
    int have = 0;
    for (size_t i = 0; i < slen; i++) {
        char b = s[i];
        if (b == ' ') {
            if (have) {
                words[nwords][cur] = '\0';
                nwords++;
                cur = 0;
                have = 0;
            }
        } else {
            words[nwords][cur++] = b;
            have = 1;
        }
    }
    if (have) {
        words[nwords][cur] = '\0';
        nwords++;
    }
}

static int word_pattern(const char *pattern, size_t plen, const char *s, size_t slen) {
    split_words(s, slen);
    if (plen != (size_t)nwords) {
        return 0;
    }

    static P2W p2w;
    static W2P w2p;
    memset(p2w.used, 0, sizeof(p2w.used));
    memset(w2p.used, 0, sizeof(w2p.used));

    for (size_t i = 0; i < plen; i++) {
        long long c = (unsigned char)pattern[i];
        const char *w = words[i];

        if (p2w.used[c]) {
            if (strcmp(p2w.val[c], w) != 0) {
                return 0;
            }
        } else {
            p2w.used[c] = 1;
            memcpy(p2w.val[c], w, strlen(w) + 1);
        }

        size_t h = w2p_slot(&w2p, w);
        if (w2p.used[h]) {
            if (w2p.val[h] != c) {
                return 0;
            }
        } else {
            w2p.used[h] = 1;
            memcpy(w2p.key[h], w, strlen(w) + 1);
            w2p.val[h] = c;
        }
    }
    return 1;
}

static char patterns[NP][PL + 1];
static char subjects[NP][SUBLEN];
static size_t sublens[NP];

int main(void) {
    char alpha[ALPHA_N];
    for (int a = 0; a < ALPHA_N; a++) {
        alpha[a] = (char)(97 + a);
    }

    for (int j = 0; j < NP; j++) {
        size_t sp = 0;
        for (int i = 0; i < PL; i++) {
            int slot = (i + j) % ALPHA_N;
            patterns[j][i] = alpha[slot];
            if (i > 0) {
                subjects[j][sp++] = ' ';
            }
            int wslot = slot;
            if (j % 2 == 1 && i == PL - 1) {
                wslot = j % ALPHA_N;
            }
            sp += (size_t)sprintf(subjects[j] + sp, "w%d", wslot);
        }
        patterns[j][PL] = '\0';
        subjects[j][sp] = '\0';
        sublens[j] = sp;
    }

    long long sink = 0;
    for (int it = 0; it < ITERS; it++) {
        int idx = (it * 3) % NP;
        if (word_pattern(patterns[idx], PL, subjects[idx], sublens[idx])) {
            sink += (long long)it + 1;
        } else {
            sink += 1;
        }
    }
    printf("%lld\n", sink);
    return 0;
}
