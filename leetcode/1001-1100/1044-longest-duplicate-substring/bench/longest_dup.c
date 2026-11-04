// LeetCode #1044: Longest Duplicate Substring -- bench, C mirror of
// longest_dup.kara (binary search on the length, rolling hash). The map
// from a window's hash to the starts with that hash is a chained hash
// table, allocated afresh on every check as the other languages' maps are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BASE 131
#define MODULUS 1000000007LL

static int same(const unsigned char *b, int64_t a, int64_t c, int64_t len) {
    for (int64_t k = 0; k < len; k++)
        if (b[a + k] != b[c + k]) return 0;
    return 1;
}

static int smaller(const unsigned char *b, int64_t a, int64_t c, int64_t len) {
    for (int64_t k = 0; k < len; k++)
        if (b[a + k] != b[c + k]) return b[a + k] < b[c + k];
    return 0;
}

// The start of the smallest window of `len` bytes that occurs twice, or -1.
static int64_t repeated_window(const unsigned char *b, int64_t n, int64_t len) {
    int64_t lead = 1;
    for (int64_t i = 1; i < len; i++) lead = lead * BASE % MODULUS;
    int64_t hash = 0;
    for (int64_t i = 0; i < len; i++) hash = (hash * BASE + b[i]) % MODULUS;
    int64_t windows = n - len + 1;
    int64_t buckets = 1;
    while (buckets < 2 * windows) buckets *= 2;
    int64_t *head = malloc(buckets * sizeof(int64_t));
    memset(head, -1, buckets * sizeof(int64_t));
    int64_t *key = malloc(windows * sizeof(int64_t));
    int64_t *at = malloc(windows * sizeof(int64_t));
    int64_t *next = malloc(windows * sizeof(int64_t));
    int64_t used = 0;
    int64_t found = -1;
    for (int64_t start = 0;; start++) {
        int64_t slot = (hash * 0x9E3779B97F4A7C15ULL) >> 1 & (buckets - 1);
        int earlier = 0;
        for (int64_t e = head[slot]; e >= 0; e = next[e])
            if (key[e] == hash && same(b, at[e], start, len)) {
                earlier = 1;
                break;
            }
        if (earlier) {
            if (found < 0 || smaller(b, start, found, len)) found = start;
        } else {
            key[used] = hash;
            at[used] = start;
            next[used] = head[slot];
            head[slot] = used++;
        }
        if (start + len == n) break;
        hash = (hash - b[start] * lead % MODULUS + MODULUS) % MODULUS;
        hash = (hash * BASE + b[start + len]) % MODULUS;
    }
    free(head);
    free(key);
    free(at);
    free(next);
    return found;
}

// The answer as the start and length of its first occurrence found.
static void longest_dup_substring(const unsigned char *b, int64_t n, int64_t *start, int64_t *length) {
    int64_t low = 1, high = n - 1;
    *start = 0;
    *length = 0;
    while (low <= high) {
        int64_t len = (low + high) / 2;
        int64_t s = repeated_window(b, n, len);
        if (s >= 0) {
            *start = s;
            *length = len;
            low = len + 1;
        } else {
            high = len - 1;
        }
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 12, N = 30000, ROUNDS = 2 };
    int64_t seed = 1044;
    static unsigned char strings[COUNT][N];
    const int64_t ks[4] = {2, 4, 8, 26};
    for (int c = 0; c < COUNT; c++) {
        int64_t k = ks[c % 4];
        for (int i = 0; i < N; i++) strings[c][i] = 'a' + next_random(&seed) % k;
        if (c % 2 == 1) {
            int64_t from = next_random(&seed) % (N / 2);
            int64_t to = N / 2 + next_random(&seed) % (N / 2 - N / 8);
            for (int i = 0; i < N / 8; i++) strings[c][to + i] = strings[c][from + i];
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t start, length;
            longest_dup_substring(strings[c], N, &start, &length);
            total += length;
            check = (check * 131 + length + 1) % 1000000007;
            for (int64_t i = 0; i < length; i++) check = (check * 131 + strings[c][start + i]) % 1000000007;
        }
    }
    printf("%d strings of %d letters, %d rounds: total length %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)check);
    return 0;
}
