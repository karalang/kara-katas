/* Benchmark harness for LeetCode #332 — Hierholzer Eulerian path.
 * Mirrors reconstruct_itinerary.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so one is hand-rolled: open addressing with linear
 * probing, keyed by the airport string (FNV-1a hash, strcmp compare), with a
 * growable destination list per slot. Destinations are stored as inline
 * fixed-width char arrays, so each edge copies its string exactly like the
 * Kara/Rust/Go/Python versions do — not as pointers into a shared pool, which
 * would skip a copy the other four all pay.
 *
 * The adjacency build appends in O(1) amortized, matching Rust's entry(), Go's
 * append(m[k], v) and Python's setdefault. The Kara mirror cannot express that
 * form — m[k].push(x) is rejected by codegen (kara ledger B-2026-07-25-5,
 * open) — so it does get-copy-push-insert at O(degree) per edge. See
 * ../README.md § Benchmarks.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAMELEN 8
#define MAPCAP 2048 /* power of two; > 2x the ~961 distinct airports */
#define M 40
#define L 24
#define ITERS 250
#define EDGES (M * (L + 1))

typedef char Name[NAMELEN];

typedef struct {
    Name key;
    unsigned char used;
    Name *dests;
    int ndest;
    int cap;
    long long cursor;
} Slot;

static Slot map_[MAPCAP];
static Name route[EDGES + 1];
static int nroute;

static size_t hash_name(const char *s) {
    size_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h ^= (unsigned char)*s;
        h *= 1099511628211ULL;
    }
    return h & (MAPCAP - 1);
}

static Slot *slot_for(const char *key) {
    size_t h = hash_name(key);
    while (map_[h].used && strcmp(map_[h].key, key) != 0) {
        h = (h + 1) & (MAPCAP - 1);
    }
    return &map_[h];
}

static void map_reset(void) {
    for (size_t i = 0; i < MAPCAP; i++) {
        if (map_[i].used) {
            free(map_[i].dests);
        }
    }
    memset(map_, 0, sizeof(map_));
}

static void adj_push(const char *from, const char *to) {
    Slot *s = slot_for(from);
    if (!s->used) {
        s->used = 1;
        snprintf(s->key, NAMELEN, "%s", from);
        s->cap = 4;
        s->dests = malloc(sizeof(Name) * (size_t)s->cap);
        s->ndest = 0;
        s->cursor = 0;
    }
    if (s->ndest == s->cap) {
        s->cap *= 2;
        s->dests = realloc(s->dests, sizeof(Name) * (size_t)s->cap);
    }
    snprintf(s->dests[s->ndest], NAMELEN, "%s", to);
    s->ndest++;
}

static int cmp_name(const void *a, const void *b) {
    return strcmp((const char *)a, (const char *)b);
}

static void visit(const char *airport) {
    for (;;) {
        Slot *s = slot_for(airport);
        if (!s->used || s->cursor >= s->ndest) {
            break;
        }
        /* Copy the destination before recursing: the slot's array may be
         * reallocated by nothing here, but the recursive call re-resolves the
         * slot, and this keeps the read independent of that. */
        Name next;
        snprintf(next, NAMELEN, "%s", s->dests[s->cursor]);
        s->cursor++;
        visit(next);
    }
    snprintf(route[nroute], NAMELEN, "%s", airport);
    nroute++;
}

static void find_itinerary(const Name *froms, const Name *tos, long long rot) {
    map_reset();
    for (long long i = 0; i < EDGES; i++) {
        long long idx = (i + rot) % EDGES;
        adj_push(froms[idx], tos[idx]);
    }

    for (size_t i = 0; i < MAPCAP; i++) {
        if (map_[i].used) {
            qsort(map_[i].dests, (size_t)map_[i].ndest, sizeof(Name), cmp_name);
        }
    }

    nroute = 0;
    visit("JFK");
    /* route currently holds the reverse itinerary; the caller walks it
     * backwards, matching the Kara version's explicit reverse loop. */
}

int main(void) {
    static Name froms[EDGES];
    static Name tos[EDGES];

    int e = 0;
    for (long long j = 0; j < M; j++) {
        Name prev;
        snprintf(prev, NAMELEN, "JFK");
        for (long long k = 0; k < L; k++) {
            Name cur;
            snprintf(cur, NAMELEN, "A%lld", j * L + k);
            snprintf(froms[e], NAMELEN, "%s", prev);
            snprintf(tos[e], NAMELEN, "%s", cur);
            e++;
            snprintf(prev, NAMELEN, "%s", cur);
        }
        snprintf(froms[e], NAMELEN, "%s", prev);
        snprintf(tos[e], NAMELEN, "JFK");
        e++;
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        find_itinerary(froms, tos, it);
        for (int i = 0; i < nroute; i++) {
            const char *s = route[nroute - 1 - i]; /* reversed */
            long long cs = 0;
            for (const char *p = s; *p; p++) {
                cs += (unsigned char)*p;
            }
            sink += (long long)(i + 1) * cs;
        }
    }
    printf("%lld\n", sink);
    return 0;
}
