/* uniqueabbr_par.c with ONE function changed — the B-2026-08-28-76 control.
 *
 * That row's most load-bearing evidence was that the C pthreads mirror ALSO
 * fails to scale on the M5 (0.76x against its own sequential lane), which read
 * as "this machine does not scale this workload in any language" and pointed
 * the diagnosis away from kara's auto-par. It is not that. The mirror's
 * `abbrev` calls `sprintf` once per punch, a million times, across 18 threads,
 * and libc formatting serializes on macOS — B-2026-09-05-23 measured exactly
 * that on the KARA lane of this same kata.
 *
 * This file is the mirror with `abbrev` writing its digits by hand and nothing
 * else touched. Measured on an M5 Pro, hyperfine 15 runs, all arms printing
 * `unique 573650`:
 *
 *     C seq                 54.34 ms   user  52.35   sys   1.28
 *     C par, sprintf        70.94 ms   user 160.58   sys 903.57   0.77x
 *     C par, manual digits   3.24 ms   user  22.30   sys   0.95  16.76x
 *
 * 21.9x between the two par lanes, from one function. The 903 ms of SYSTEM
 * time on a 71 ms run is the mechanism showing through; `/usr/bin/time -l`
 * agrees, 865 involuntary context switches against 63.
 *
 * So the C mirror is not evidence about partitioning, and with the formatting
 * gone it gets 16.76x on ~15.7 cores — close to what the hardware offers. Keep
 * both files: the sprintf one is what the bench harness measures and what the
 * corpus row reports, and this one is why that number means what it means.
 *
 *   clang -O3 uniqueabbr_par_nofmt.c -o nofmt -lpthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include <unistd.h>

#define DICT_N   3000
#define POOL_N   20000
#define PUNCHES  1000000
#define TABLE_SZ 16384          /* power of two, > 2x the distinct abbreviations */
#define MAXW     16

static const char *LETTERS = "abcdefghijklmnopqrstuvwxyz";

typedef struct {
    char key[MAXW];             /* abbreviation; empty means a free slot */
    char word[MAXW];            /* the sole word, when conflicted == 0 */
    int  used;
    int  conflicted;
} slot;

static slot table[TABLE_SZ];

static uint64_t fnv1a(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    while (*s) {
        h ^= (unsigned char)*s++;
        h *= 1099511628211ULL;
    }
    return h;
}

/* Returns the slot for `key`, inserting an empty one if absent. */
static slot *slot_for(const char *key) {
    size_t i = (size_t)(fnv1a(key) & (TABLE_SZ - 1));
    for (;;) {
        if (!table[i].used) {
            table[i].used = 1;
            strcpy(table[i].key, key);
            return &table[i];
        }
        if (strcmp(table[i].key, key) == 0) return &table[i];
        i = (i + 1) & (TABLE_SZ - 1);
    }
}

/* Read-only probe: NULL when the abbreviation is absent. */
static slot *slot_find(const char *key) {
    size_t i = (size_t)(fnv1a(key) & (TABLE_SZ - 1));
    for (;;) {
        if (!table[i].used) return NULL;
        if (strcmp(table[i].key, key) == 0) return &table[i];
        i = (i + 1) & (TABLE_SZ - 1);
    }
}

/* ONE-LINE VARIANT for B-2026-08-28-76: the identical function with its digits
 * written by hand instead of through libc. Same output for every input this
 * program produces (word lengths are 3..10, so n-2 is 1..8), and the general
 * loop is kept rather than a single-digit shortcut so the two differ only in
 * WHO formats. */
static void abbrev(const char *w, char *out) {
    size_t n = strlen(w);
    if (n <= 2) { strcpy(out, w); return; }
    size_t mid = n - 2;
    char digits[24];
    int d = 0;
    do { digits[d++] = (char)('0' + (mid % 10)); mid /= 10; } while (mid);
    int k = 0;
    out[k++] = w[0];
    while (d > 0) out[k++] = digits[--d];
    out[k++] = w[n - 1];
    out[k] = '\0';
}

static int64_t next_rand(int64_t state) {
    return (state * 1103515245 + 12345) & 2147483647;
}

#define MAX_THREADS 64

typedef struct {
    int64_t lo, hi;
    const char (*pool)[MAXW];
    int64_t count;
} targ;

/* One contiguous slice of the punch loop. Reads `table` only. */
static void *punch_worker(void *p) {
    targ *t = (targ *)p;
    char a[MAXW];
    int64_t local = 0;
    for (int64_t i = t->lo; i < t->hi; i++) {
        const char *word = t->pool[i % POOL_N];
        abbrev(word, a);
        slot *s = slot_find(a);
        int u;
        if (s == NULL)          u = 1;
        else if (s->conflicted) u = 0;
        else                    u = strcmp(s->word, word) == 0;
        if (u) local++;
    }
    t->count = local;
    return NULL;
}

int main(void) {
    static char dict[DICT_N][MAXW];
    static char pool[POOL_N][MAXW];
    int64_t seed = 12345;
    char a[MAXW];

    for (int i = 0; i < DICT_N; i++) {
        seed = next_rand(seed);
        int64_t n = 3 + ((seed / 65536) % 8);
        for (int64_t j = 0; j < n; j++) {
            seed = next_rand(seed);
            dict[i][j] = LETTERS[(seed / 65536) % 26];
        }
        dict[i][n] = '\0';
    }

    for (int i = 0; i < DICT_N; i++) {
        abbrev(dict[i], a);
        slot *s = slot_for(a);
        if (s->word[0] == '\0' && !s->conflicted) {
            strcpy(s->word, dict[i]);                 /* -> Sole(word) */
        } else if (!s->conflicted && strcmp(s->word, dict[i]) != 0) {
            s->conflicted = 1;                        /* -> Conflicted */
            s->word[0] = '\0';
        }
    }

    for (int i = 0; i < POOL_N; i++) {
        if (i % 2 == 0) {
            strcpy(pool[i], dict[(i * 7) % DICT_N]);
        } else {
            seed = next_rand(seed);
            int64_t n = 3 + ((seed / 65536) % 8);
            for (int64_t j = 0; j < n; j++) {
                seed = next_rand(seed);
                pool[i][j] = LETTERS[(seed / 65536) % 26];
            }
            pool[i][n] = '\0';
        }
    }

    int64_t unique_count = 0;
    long nthreads = sysconf(_SC_NPROCESSORS_ONLN);
    if (nthreads < 1) nthreads = 1;
    if (nthreads > MAX_THREADS) nthreads = MAX_THREADS;

    pthread_t tid[MAX_THREADS];
    targ args[MAX_THREADS];
    int64_t per = PUNCHES / nthreads;
    for (long t = 0; t < nthreads; t++) {
        args[t].lo = t * per;
        args[t].hi = (t == nthreads - 1) ? PUNCHES : (t + 1) * per;
        args[t].pool = (const char (*)[MAXW])pool;
        args[t].count = 0;
        pthread_create(&tid[t], NULL, punch_worker, &args[t]);
    }
    for (long t = 0; t < nthreads; t++) {
        pthread_join(tid[t], NULL);
        unique_count += args[t].count;   /* associative: order cannot matter */
    }

    printf("unique %lld\n", (long long)unique_count);
    return 0;
}
