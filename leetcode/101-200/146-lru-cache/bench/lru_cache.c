#include <stdio.h>
#include <stdlib.h>

/* The key -> pool-index map is hand-rolled (C has no stdlib hash map) as an
 * open-addressing, linear-probing table shaped to match the runtime's
 * Map[i64,i64]:
 *
 *   - heap-allocated, capacity 16 initially, power of two;
 *   - grow (double + full rehash, dropping tombstones) when
 *     (len + tombstones + 1) * 4 > capacity * 3 -- the runtime's exact trigger;
 *   - insert reuses the first tombstone in the probe chain and decrements the
 *     tombstone count when it fills one, matching find_insert_slot / insert;
 *   - remove tombstones the bucket, matching the runtime;
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply).
 *
 * The previous version was a direct-address array -- `keypos[key]` indexed by
 * the key itself over a 4096-wide range. That is not a fast map, it is the
 * absence of one: no hash, no probe, no growth, and it only works because the
 * key range happens to be bounded. Rust, Go and the kata all hash.
 *
 * Tombstone reuse is load-bearing here and worth stating, because this kata
 * looks like it should trip B-2026-07-31-21 (Map capacity grows with total
 * removals, not live size) and does not. Every eviction removes a key and
 * every miss inserts one, ~12M removals over the run -- but the key range is
 * only 4096 wide, so a re-admitted key lands on the tombstone its own earlier
 * eviction left and the counter comes back down. Capacity settles at 2048 and
 * stays; measured kara peak RSS is 1.4 MB. A version of this workload drawing
 * from an unbounded key space would grow without bound instead. */

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

#define BUCKET_EMPTY 0
#define BUCKET_OCCUPIED 1
#define BUCKET_TOMBSTONE 2

static long *m_keys;
static long *m_vals;
static unsigned char *m_status;
static size_t m_cap;
static size_t m_len;
static size_t m_tombs;

static void map_alloc(size_t cap) {
    m_cap = cap;
    m_len = 0;
    m_tombs = 0;
    m_keys = malloc(cap * sizeof(long));
    m_vals = malloc(cap * sizeof(long));
    m_status = calloc(cap, 1); /* BUCKET_EMPTY == 0 */
}

/* Mirrors find_insert_slot: target slot plus whether the key was already
 * present, reusing the first tombstone in the probe chain. */
static size_t map_insert_slot(long key, int *exists) {
    size_t mask = m_cap - 1;
    size_t start = (size_t)((unsigned long)key * FXHASH_SEED) & mask;
    size_t first_tomb = (size_t)-1;
    for (size_t i = 0; i < m_cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = m_status[slot];
        if (st == BUCKET_EMPTY) {
            *exists = 0;
            return first_tomb != (size_t)-1 ? first_tomb : slot;
        }
        if (st == BUCKET_TOMBSTONE) {
            if (first_tomb == (size_t)-1) first_tomb = slot;
        } else if (m_keys[slot] == key) {
            *exists = 1;
            return slot;
        }
    }
    *exists = 0;
    return first_tomb != (size_t)-1 ? first_tomb : 0;
}

/* Mirrors resize + rehash_from: double, replay only OCCUPIED slots, drop
 * tombstones. Never shrinks. */
static void map_resize(void) {
    long *ok = m_keys;
    long *ov = m_vals;
    unsigned char *os = m_status;
    size_t ocap = m_cap;

    map_alloc(ocap * 2);

    size_t mask = m_cap - 1;
    for (size_t i = 0; i < ocap; i++) {
        if (os[i] != BUCKET_OCCUPIED) continue;
        size_t slot = (size_t)((unsigned long)ok[i] * FXHASH_SEED) & mask;
        while (m_status[slot] != BUCKET_EMPTY) {
            slot = (slot + 1) & mask;
        }
        m_status[slot] = BUCKET_OCCUPIED;
        m_keys[slot] = ok[i];
        m_vals[slot] = ov[i];
        m_len++;
    }
    free(ok);
    free(ov);
    free(os);
}

static void map_insert(long key, long val) {
    if ((m_len + m_tombs + 1) * 4 > m_cap * 3) {
        map_resize();
    }
    int exists;
    size_t slot = map_insert_slot(key, &exists);
    if (!exists) {
        if (m_status[slot] == BUCKET_TOMBSTONE) m_tombs--;
        m_status[slot] = BUCKET_OCCUPIED;
        m_keys[slot] = key;
        m_len++;
    }
    m_vals[slot] = val;
}

/* Returns the stored value, or `dflt` when the key is absent. */
static long map_get_or(long key, long dflt) {
    size_t mask = m_cap - 1;
    size_t start = (size_t)((unsigned long)key * FXHASH_SEED) & mask;
    for (size_t i = 0; i < m_cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = m_status[slot];
        if (st == BUCKET_EMPTY) return dflt;
        if (st == BUCKET_OCCUPIED && m_keys[slot] == key) return m_vals[slot];
    }
    return dflt;
}

static void map_remove(long key) {
    size_t mask = m_cap - 1;
    size_t start = (size_t)((unsigned long)key * FXHASH_SEED) & mask;
    for (size_t i = 0; i < m_cap; i++) {
        size_t slot = (start + i) & mask;
        unsigned char st = m_status[slot];
        if (st == BUCKET_EMPTY) return;
        if (st == BUCKET_OCCUPIED && m_keys[slot] == key) {
            m_status[slot] = BUCKET_TOMBSTONE;
            m_len--;
            m_tombs++;
            return;
        }
    }
}

int main(void) {
    long cap = 1024, key_range = 4096, ops = 32000000;


    // Index-pool doubly-linked list: 0 = head sentinel, 1 = tail sentinel,
    // real nodes at 2 .. cap+2. prev/next are pool indices.
    long pool = cap + 2;
    long *nkey  = malloc(pool * sizeof(long));
    long *nval  = malloc(pool * sizeof(long));
    long *nprev = malloc(pool * sizeof(long));
    long *nnext = malloc(pool * sizeof(long));
    for (long i = 0; i < pool; i++) { nkey[i] = -1; nval[i] = 0; nprev[i] = -1; nnext[i] = -1; }
    nnext[0] = 1; nprev[1] = 0;   // empty list: head <-> tail

    map_alloc(INITIAL_CAPACITY);

    long size = 0;
    long sink = 0;
    long state = 12345;
    for (long t = 0; t < ops; t++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long h1 = state >> 16;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long h2 = state >> 16;
        long key = h2 % key_range;

        if (h1 % 2 == 0) {
            // get(key)
            long r;
            long idx = map_get_or(key, -1);
            if (idx >= 0) {
                // move_front(idx): unlink then push_front
                nnext[nprev[idx]] = nnext[idx];
                nprev[nnext[idx]] = nprev[idx];
                long first = nnext[0];
                nprev[idx] = 0; nnext[idx] = first;
                nprev[first] = idx; nnext[0] = idx;
                r = nval[idx];
            } else {
                r = -1;
            }
            sink += r + 1;
        } else {
            // put(key, v)
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long h3 = state >> 16;
            long v = h3;
            long idx = map_get_or(key, -1);
            if (idx >= 0) {
                nval[idx] = v;
                nnext[nprev[idx]] = nnext[idx];
                nprev[nnext[idx]] = nprev[idx];
                long first = nnext[0];
                nprev[idx] = 0; nnext[idx] = first;
                nprev[first] = idx; nnext[0] = idx;
            } else {
                if (size < cap) {
                    idx = 2 + size;
                    size += 1;
                } else {
                    long lru = nprev[1];
                    nnext[nprev[lru]] = nnext[lru];
                    nprev[nnext[lru]] = nprev[lru];
                    map_remove(nkey[lru]);
                    idx = lru;
                }
                nkey[idx] = key; nval[idx] = v;
                map_insert(key, idx);
                long first = nnext[0];
                nprev[idx] = 0; nnext[idx] = first;
                nprev[first] = idx; nnext[0] = idx;
            }
        }
    }
    printf("%ld\n", sink);
    free(nkey); free(nval); free(nprev); free(nnext);
    free(m_keys); free(m_vals); free(m_status);
    return 0;
}
