/* Benchmark mirror for LeetCode #245 - Shortest Word Distance III.
 *
 * Same algorithm, same LCG, same sink as the Kara/Rust/Go/Python mirrors, and
 * the same workload as #243's bench so the two are directly comparable. Half
 * the punches are same-word queries - the case #243 cannot answer.
 *
 * Words carry an explicit length and compare length-then-memcmp rather than
 * strcmp, matching #243: every word here is the same 9 bytes, so the length
 * check never discriminates, and a strcmp mirror would measure a different
 * primitive (walk-to-NUL with no length available).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define VOCAB_N 256
#define N 20000
#define ITERS 2000
#define WORD_LEN 9

typedef struct {
    const char *p;
    int len;
} Str;

static int str_eq(Str a, Str b) {
    return a.len == b.len && memcmp(a.p, b.p, (size_t)a.len) == 0;
}

static long shortest_word_distance(const Str *words, long n, Str word1, Str word2) {
    int same = str_eq(word1, word2);
    long best = n;
    long prev = -1;
    for (long i = 0; i < n; i++) {
        if (str_eq(words[i], word1) || str_eq(words[i], word2)) {
            if (prev >= 0 && (same || !str_eq(words[prev], words[i]))) {
                if (i - prev < best) best = i - prev;
            }
            prev = i;
        }
    }
    return best;
}

static long lcg(long state) {
    return (state * 1103515245L + 12345L) & 2147483647L;
}

int main(void) {
    static const char alpha[4] = {'a', 'b', 'c', 'd'};

    char (*vocab_buf)[WORD_LEN + 1] = malloc(VOCAB_N * (WORD_LEN + 1));
    Str *vocab = malloc(VOCAB_N * sizeof(Str));
    for (int v = 0; v < VOCAB_N; v++) {
        memcpy(vocab_buf[v], "delta", 5);
        vocab_buf[v][5] = alpha[(v / 64) % 4];
        vocab_buf[v][6] = alpha[(v / 16) % 4];
        vocab_buf[v][7] = alpha[(v / 4) % 4];
        vocab_buf[v][8] = alpha[v % 4];
        vocab_buf[v][9] = '\0';
        vocab[v].p = vocab_buf[v];
        vocab[v].len = WORD_LEN;
    }

    /* Each slot gets its OWN copy, so equality never sees shared pointers. */
    Str *list = malloc(N * sizeof(Str));
    long state = 1;
    for (long i = 0; i < N; i++) {
        state = lcg(state);
        const Str *src = &vocab[(state / 65536) % VOCAB_N];
        char *copy = malloc(WORD_LEN + 1);
        memcpy(copy, src->p, WORD_LEN + 1);
        list[i].p = copy;
        list[i].len = src->len;
    }

    long acc = 0;
    long qstate = 7;
    for (long k = 0; k < ITERS; k++) {
        qstate = lcg(qstate);
        long a = (qstate / 65536) % VOCAB_N;
        qstate = lcg(qstate);
        long b = (qstate / 65536) % VOCAB_N;
        if (b == a) b = (b + 1) % VOCAB_N;
        long d;
        if (k % 2 == 0) d = shortest_word_distance(list, N, vocab[a], vocab[a]);
        else            d = shortest_word_distance(list, N, vocab[a], vocab[b]);
        acc = (acc * 131 + d) % 1000000007L;
    }
    printf("%ld\n", acc);
    return 0;
}
