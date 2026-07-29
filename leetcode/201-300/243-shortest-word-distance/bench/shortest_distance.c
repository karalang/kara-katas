/* Benchmark harness for LeetCode #243 — Shortest Word Distance.
 * Mirrors shortest_distance.kara algorithm-for-algorithm.
 *
 * On the string representation — this is the one place a C mirror can quietly
 * stop measuring the same operation as the other four. C's reflex here is
 * `strcmp`, which carries no length and must walk to a NUL or a mismatch. The
 * other four languages all hold (pointer, length) and compare the length first.
 * A strcmp mirror would therefore be benchmarking a DIFFERENT primitive, and
 * since every word here is the same 9 bytes long the length check never fires
 * anyway — the difference would be pure representation overhead, not algorithm.
 *
 * So `Str` carries an explicit length and `str_eq` does length-then-memcmp,
 * exactly what Rust's `String == &str`, Go's `==` and kāra's `String ==` do.
 *
 * Each of the 20,000 slots gets its OWN copy of its word (its own row of
 * `pool`), matching the `.clone()` in the kāra and Rust mirrors, so no lane can
 * shortcut an equality test by noticing the operands share a data pointer.
 */

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#define VOCAB_N 256
#define N 20000
#define ITERS 2000
#define WLEN 9

typedef struct {
    const char *p;
    int32_t len;
} Str;

static inline int str_eq(Str a, Str b) {
    return a.len == b.len && memcmp(a.p, b.p, (size_t)a.len) == 0;
}

static long long shortest_distance(const Str *words, long long n, Str w1, Str w2) {
    long long last1 = -1, last2 = -1;
    long long best = n;
    for (long long i = 0; i < n; i++) {
        if (str_eq(words[i], w1)) {
            last1 = i;
            if (last2 >= 0) {
                long long d = last1 - last2;
                best = d < best ? d : best;
            }
        } else if (str_eq(words[i], w2)) {
            last2 = i;
            if (last1 >= 0) {
                long long d = last2 - last1;
                best = d < best ? d : best;
            }
        }
    }
    return best;
}

/* Overflow-free 31-bit LCG; every draw uses bits 16..23. */
static long long lcg(long long state) {
    return (state * 1103515245LL + 12345LL) & 2147483647LL;
}

static char vocab_buf[VOCAB_N][WLEN + 1];
static Str vocab[VOCAB_N];
static char pool[N][WLEN + 1];
static Str list[N];

int main(void) {
    const char alpha[4] = {'a', 'b', 'c', 'd'};

    for (long long v = 0; v < VOCAB_N; v++) {
        memcpy(vocab_buf[v], "delta", 5);
        vocab_buf[v][5] = alpha[(v / 64) % 4];
        vocab_buf[v][6] = alpha[(v / 16) % 4];
        vocab_buf[v][7] = alpha[(v / 4) % 4];
        vocab_buf[v][8] = alpha[v % 4];
        vocab_buf[v][9] = '\0';
        vocab[v].p = vocab_buf[v];
        vocab[v].len = WLEN;
    }

    long long state = 1;
    for (long long i = 0; i < N; i++) {
        state = lcg(state);
        long long j = (state / 65536) % VOCAB_N;
        memcpy(pool[i], vocab_buf[j], WLEN + 1);
        list[i].p = pool[i];
        list[i].len = WLEN;
    }

    long long acc = 0;
    long long qstate = 7;
    for (long long k = 0; k < ITERS; k++) {
        qstate = lcg(qstate);
        long long a = (qstate / 65536) % VOCAB_N;
        qstate = lcg(qstate);
        long long b = (qstate / 65536) % VOCAB_N;
        if (b == a) {
            b = (b + 1) % VOCAB_N;
        }
        long long d = shortest_distance(list, N, vocab[a], vocab[b]);
        acc = (acc * 131 + d) % 1000000007LL;
    }
    printf("%lld\n", acc);
    return 0;
}
