// LeetCode #2213: Longest Substring of One Repeating Character -- bench
// mirror of repeating.kara: a segment tree over the letters, each node
// keeping the longest run from its start, from its end and inside.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *letters;
static long *prefix, *suffix, *best;

static long max(long a, long b) { return a > b ? a : b; }

static void pull(long node, long lo, long hi) {
    long mid = (lo + hi) / 2, left = 2 * node, right = 2 * node + 1;
    int joined = letters[mid] == letters[mid + 1];
    prefix[node] = joined && prefix[left] == mid - lo + 1 ? prefix[left] + prefix[right] : prefix[left];
    suffix[node] = joined && suffix[right] == hi - mid ? suffix[right] + suffix[left] : suffix[right];
    best[node] = max(best[left], best[right]);
    if (joined) best[node] = max(best[node], suffix[left] + prefix[right]);
}

static void build(long node, long lo, long hi) {
    if (lo == hi) {
        prefix[node] = suffix[node] = best[node] = 1;
        return;
    }
    long mid = (lo + hi) / 2;
    build(2 * node, lo, mid);
    build(2 * node + 1, mid + 1, hi);
    pull(node, lo, hi);
}

static void update(long node, long lo, long hi, long at) {
    if (lo == hi) return;
    long mid = (lo + hi) / 2;
    if (at <= mid) update(2 * node, lo, mid, at);
    else update(2 * node + 1, mid + 1, hi, at);
    pull(node, lo, hi);
}

static void longest_repeating(const char *s, long n, const char *qc, const long *qi, long k, long *lengths) {
    letters = malloc(n);
    memcpy(letters, s, n);
    prefix = calloc(4 * n, sizeof(long));
    suffix = calloc(4 * n, sizeof(long));
    best = calloc(4 * n, sizeof(long));
    build(1, 0, n - 1);
    for (long q = 0; q < k; q++) {
        letters[qi[q]] = qc[q];
        update(1, 0, n - 1, qi[q]);
        lengths[q] = best[1];
    }
    free(letters); free(prefix); free(suffix); free(best);
}

static long seed = 2213;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

#define N 100000
int main(void) {
    static char s[6][N], qc[6][N];
    static long qi[6][N], lengths[N];
    long alphabets[3] = {2, 3, 26};
    for (int w = 0; w < 6; w++) {
        // 10^5 letters from 2, 3 and 26 in turn, with 10^5 queries
        long a = alphabets[w % 3];
        for (long i = 0; i < N; i++) s[w][i] = 'a' + next_random() % a;
        for (long i = 0; i < N; i++) qc[w][i] = 'a' + next_random() % a;
        for (long i = 0; i < N; i++) qi[w][i] = next_random() % N;
    }
    long check = 0;
    for (int w = 0; w < 6; w++) {
        longest_repeating(s[w], N, qc[w], qi[w], N, lengths);
        for (long i = 0; i < N; i++) check = (check * 31 + lengths[i]) % 1000000007;
    }
    printf("6 words of 10^5: checksum %ld\n", check);
    return 0;
}
