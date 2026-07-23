#include <stdio.h>
#include <stdlib.h>

// Open-addressing linear-probe map keyed by i64 bucket id. A per-slot generation
// stamp gives an O(1) logical clear between checks (bump `cur`), so no memset
// distorts the measured map churn. Deletion uses tombstones (also generation-
// stamped). The table is sized so occupied + tombstones stay well under load in a
// single window scan.
#define LOG2SIZE 16
#define TSIZE (1 << LOG2SIZE)
#define TMASK (TSIZE - 1)

static long g_gen[TSIZE];
static long g_key[TSIZE];
static long g_val[TSIZE];
static char g_st[TSIZE]; // 1 = occupied, 2 = tombstone (only meaningful when gen == cur)
static long cur = 0;

static long hash_idx(long key) {
    unsigned long h = (unsigned long)key * 11400714819323198485UL;
    return (long)(h >> (64 - LOG2SIZE)) & TMASK;
}

static void map_clear(void) { cur++; }

static void map_insert(long key, long val) {
    long h = hash_idx(key);
    long slot = -1;
    for (long probe = 0;; probe++) {
        long i = (h + probe) & TMASK;
        if (g_gen[i] != cur) { // empty
            if (slot == -1) slot = i;
            break;
        }
        if (g_st[i] == 2) { // tombstone
            if (slot == -1) slot = i;
            continue;
        }
        if (g_key[i] == key) { // overwrite
            g_val[i] = val;
            return;
        }
    }
    g_gen[slot] = cur;
    g_st[slot] = 1;
    g_key[slot] = key;
    g_val[slot] = val;
}

// Returns 1 and writes *out if present, else 0.
static int map_get(long key, long *out) {
    long h = hash_idx(key);
    for (long probe = 0;; probe++) {
        long i = (h + probe) & TMASK;
        if (g_gen[i] != cur) return 0; // empty
        if (g_st[i] == 1 && g_key[i] == key) {
            *out = g_val[i];
            return 1;
        }
    }
}

static void map_remove(long key) {
    long h = hash_idx(key);
    for (long probe = 0;; probe++) {
        long i = (h + probe) & TMASK;
        if (g_gen[i] != cur) return; // empty -> not present
        if (g_st[i] == 1 && g_key[i] == key) {
            g_st[i] = 2; // tombstone
            return;
        }
    }
}

static long abs_i64(long x) { return x < 0 ? -x : x; }

static long bucket_of(long x, long w) {
    if (x >= 0) return x / w;
    return (x + 1) / w - 1;
}

static int near_value(long b, long x, long t) {
    long v;
    if (map_get(b, &v) && abs_i64(x - v) <= t) return 1;
    return 0;
}

static int contains(const long *nums, long n, long k, long t) {
    if (k <= 0) return 0;
    long w = t + 1;
    map_clear();
    for (long i = 0; i < n; i++) {
        long x = nums[i];
        long b = bucket_of(x, w);
        if (near_value(b, x, t)) return 1;
        if (near_value(b - 1, x, t)) return 1;
        if (near_value(b + 1, x, t)) return 1;
        map_insert(b, x);
        if (i >= k) {
            long old = nums[i - k];
            map_remove(bucket_of(old, w));
        }
    }
    return 0;
}

int main(void) {
    long n = 20000;
    long pairs = 800;
    long valrange = 8000000;
    long half = 4000000;

    long *nums = malloc(n * sizeof(long));
    long state = 12345;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        nums[c] = (state % valrange) - half;
    }

    long sink = 0;
    for (long p = 0; p < pairs; p++) {
        long k = 32 + (p % 512);
        long t = p % 3;
        if (contains(nums, n, k, t)) sink++;
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}
