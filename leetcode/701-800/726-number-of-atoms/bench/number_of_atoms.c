#include <stdio.h>
#include <stdlib.h>

/* The element-count map is hand-rolled (C has no stdlib hash map) as an
 * open-addressing, linear-probing table shaped to match the runtime's
 * Map[i64,i64]: heap-allocated per pass like the kata's `Map.new()` and freed
 * after, capacity 16 initially, power of two, doubling with a full rehash when
 * (len + 1) * 4 > capacity * 3 -- the runtime map's 75% load factor -- and
 * FxHash with the same seed the compiler synthesizes (a single zext + multiply
 * for a <= 8-byte primitive key).
 *
 * The previous version was `mapc[id]`, a direct-address array over the 24-wide
 * id range, zeroed per pass. That is not a fast map, it is the absence of one:
 * no hash, no probe, no growth, and it only works because element ids happen to
 * be small and dense. Rust, Go and the kata all hash. */

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

static long *m_keys;
static long *m_vals;
static unsigned char *m_used;
static size_t m_cap;
static size_t m_len;

static void map_init(void) {
    m_cap = INITIAL_CAPACITY;
    m_len = 0;
    m_keys = malloc(m_cap * sizeof(long));
    m_vals = malloc(m_cap * sizeof(long));
    m_used = calloc(m_cap, 1);
}

static void map_free(void) {
    free(m_keys);
    free(m_vals);
    free(m_used);
}

static size_t map_slot(long k) {
    size_t mask = m_cap - 1;
    size_t h = (size_t)((unsigned long)k * FXHASH_SEED) & mask;
    while (m_used[h] && m_keys[h] != k) {
        h = (h + 1) & mask;
    }
    return h;
}

static long map_get_or(long k, long dflt) {
    size_t h = map_slot(k);
    return m_used[h] ? m_vals[h] : dflt;
}

static void map_grow(void) {
    long *ok = m_keys;
    long *ov = m_vals;
    unsigned char *ou = m_used;
    size_t ocap = m_cap;

    m_cap = ocap * 2;
    m_keys = malloc(m_cap * sizeof(long));
    m_vals = malloc(m_cap * sizeof(long));
    m_used = calloc(m_cap, 1);

    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            size_t h = map_slot(ok[i]);
            m_used[h] = 1;
            m_keys[h] = ok[i];
            m_vals[h] = ov[i];
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

static void map_insert(long k, long v) {
    size_t h = map_slot(k);
    if (m_used[h]) {
        m_vals[h] = v;
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m_len + 1) * 4 > m_cap * 3) {
        map_grow();
        h = map_slot(k);
    }
    m_used[h] = 1;
    m_keys[h] = k;
    m_vals[h] = v;
    m_len++;
}

static int is_upper(int b) { return b >= 'A' && b <= 'Z'; }
static int is_lower(int b) { return b >= 'a' && b <= 'z'; }
static int is_digit(int b) { return b >= '0' && b <= '9'; }

static long draw_hi(long *state) {
    *state = (*state * 1103515245L + 12345L) & 2147483647L;
    return *state >> 16;
}

int main(void) {
    long num_chunks = 20000, passes = 400, id_range = 24;

    long capbuf = num_chunks * 16 + 16;
    unsigned char *buf = malloc(capbuf);
    long *dpos = malloc(capbuf * sizeof(long));
    long blen = 0, ndig = 0;
    long state = 12345;

    for (long ch = 0; ch < num_chunks; ch++) {
        long tt = draw_hi(&state) % 5;
        // element / mult emitters (inline)
        #define ELEM() do { \
            long du = draw_hi(&state); \
            buf[blen++] = (unsigned char)('A' + du % 6); \
            if ((du / 6) % 2 == 0) { long dl = draw_hi(&state); buf[blen++] = (unsigned char)('a' + dl % 3); } \
            long dc = draw_hi(&state); buf[blen++] = (unsigned char)('1' + dc % 9); dpos[ndig++] = blen - 1; \
        } while (0)
        #define MULT() do { long dm = draw_hi(&state); buf[blen++] = (unsigned char)('0' + 2 + dm % 8); dpos[ndig++] = blen - 1; } while (0)
        if (tt == 0) { ELEM(); }
        else if (tt == 1) { ELEM(); ELEM(); }
        else if (tt == 2) { buf[blen++] = '('; ELEM(); ELEM(); buf[blen++] = ')'; MULT(); }
        else if (tt == 3) { buf[blen++] = '('; ELEM(); buf[blen++] = '('; ELEM(); ELEM(); buf[blen++] = ')'; MULT(); buf[blen++] = ')'; MULT(); }
        else { buf[blen++] = '('; ELEM(); ELEM(); ELEM(); buf[blen++] = ')'; MULT(); }
    }

    long n = blen, ndg = ndig;
    long max_emit = 3 * num_chunks + 16;
    long *nid = malloc(max_emit * sizeof(long));
    long *cnt = malloc(max_emit * sizeof(long));
    long *pst = malloc(max_emit * sizeof(long));

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long pos = dpos[p % ndg];
        buf[pos] = (unsigned char)('1' + (((long)buf[pos] - '1' + 1) % 9));

        long ne = 0, ps = 0, i = 0;
        while (i < n) {
            unsigned char b = buf[i];
            if (b == '(') {
                pst[ps++] = ne;
                i++;
            } else if (b == ')') {
                i++;
                long mult = 0; int have = 0;
                while (i < n && is_digit(buf[i])) { mult = mult * 10 + (buf[i] - '0'); have = 1; i++; }
                if (!have) mult = 1;
                long start = pst[--ps];
                for (long k = start; k < ne; k++) cnt[k] *= mult;
            } else if (is_upper(b)) {
                long up = b - 'A';
                i++;
                long low = 0;
                if (i < n && is_lower(buf[i])) { low = (buf[i] - 'a') + 1; i++; }
                long id = up * 4 + low;
                long c = 0; int have = 0;
                while (i < n && is_digit(buf[i])) { c = c * 10 + (buf[i] - '0'); have = 1; i++; }
                if (!have) c = 1;
                nid[ne] = id; cnt[ne] = c; ne++;
            } else {
                i++;
            }
        }

        map_init();
        for (long e = 0; e < ne; e++) {
            map_insert(nid[e], map_get_or(nid[e], 0) + cnt[e]);
        }
        long checksum = 0;
        for (long z = 0; z < id_range; z++) checksum += z * map_get_or(z, 0);
        map_free();
        sink += checksum;
    }
    printf("%ld\n", sink);
    free(buf); free(dpos); free(nid); free(cnt); free(pst);
    return 0;
}
