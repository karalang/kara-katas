/* Benchmark harness for LeetCode #128 — Longest Consecutive Sequence.
 * Mirrors longest_consecutive.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash set, so one is hand-rolled: open addressing with linear
 * probing over i64 keys. The set is insert-only within a call — this algorithm
 * never deletes — so there are no tombstones and no probe-chain growth (the
 * defect that made #291's first C mirror 3.1x too slow).
 *
 * Deliberately a hash set and NOT a direct-address bitset, even though the
 * values fall in a known 25 000-wide range and a bitset would be far faster.
 * A bitset is a different data structure than the Kara/Rust/Go/Python sets and
 * would make the C column meaningless as a comparison.
 */

#include <stdio.h>
#include <string.h>

#define NP 8
#define N 20000
#define CAPV 25000
#define ITERS 150
#define SCAP 65536 /* power of two; > 3x the 20 000-element working set */

static long long keys[SCAP];
static unsigned char used[SCAP];

static size_t slot_for(long long k) {
    size_t h = (size_t)((unsigned long long)k * 1099511628211ULL) & (SCAP - 1);
    while (used[h] && keys[h] != k) {
        h = (h + 1) & (SCAP - 1);
    }
    return h;
}

static void set_insert(long long k) {
    size_t h = slot_for(k);
    used[h] = 1;
    keys[h] = k;
}

static int set_has(long long k) { return used[slot_for(k)]; }

static long long longest_consecutive(const long long *nums, long long len) {
    memset(used, 0, sizeof(used));
    for (long long i = 0; i < len; i++) {
        set_insert(nums[i]);
    }
    long long best = 0;
    for (long long i = 0; i < len; i++) {
        long long v = nums[i];
        if (!set_has(v - 1)) {
            long long length = 1;
            long long cur = v;
            while (set_has(cur + 1)) {
                cur++;
                length++;
            }
            if (length > best) {
                best = length;
            }
        }
    }
    return best;
}

static long long arrays[NP][N];

static void lcg(long long seed, long long n, long long cap, long long *out) {
    long long x = seed;
    for (long long k = 0; k < n; k++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        out[k] = x % cap;
    }
}

int main(void) {
    for (long long j = 0; j < NP; j++) {
        lcg(j + 1, N, CAPV, arrays[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink += longest_consecutive(arrays[idx], N);
    }
    printf("%lld\n", sink);
    return 0;
}
