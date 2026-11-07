// LeetCode #1062: Longest Repeating Substring -- the benchmark, the same
// binary search and rolling hash as lrs.kara. The map from a hash to the
// starts holding it is an open-addressed table whose slots keep a chain of
// starts.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL
#define BASE 131LL

static int64_t *keys, *heads, *next_start;
static size_t cap;

// Whether two starts in `s` hold the same `len` bytes.
static int twice(const unsigned char *s, int64_t n, int64_t len) {
    if (len == 0) return 1;
    int64_t top = 1;
    for (int64_t i = 1; i < len; i++) top = top * BASE % MOD;
    memset(heads, 0xff, cap * sizeof(int64_t));
    int64_t hash = 0;
    for (int64_t i = 0; i < n; i++) {
        if (i >= len) hash = (hash - s[i - len] * top % MOD + MOD) % MOD;
        hash = (hash * BASE + s[i]) % MOD;
        if (i + 1 >= len) {
            int64_t start = i + 1 - len;
            size_t slot = (size_t)(hash * 0x9E3779B97F4A7C15ULL >> 20) & (cap - 1);
            while (heads[slot] >= 0 && keys[slot] != hash) slot = (slot + 1) & (cap - 1);
            for (int64_t other = heads[slot]; other >= 0; other = next_start[other]) {
                if (memcmp(s + other, s + start, len) == 0) return 1;
            }
            keys[slot] = hash;
            next_start[start] = heads[slot];
            heads[slot] = start;
        }
    }
    return 0;
}

static int64_t longest_repeating(const char *str) {
    const unsigned char *s = (const unsigned char *)str;
    int64_t n = (int64_t)strlen(str);
    cap = 1;
    while (cap < 2 * (size_t)n + 2) cap <<= 1;
    keys = malloc(cap * sizeof(int64_t));
    heads = malloc(cap * sizeof(int64_t));
    next_start = malloc((n + 1) * sizeof(int64_t));
    // twice(lo) and not twice(hi)
    int64_t lo = 0, hi = n;
    while (hi - lo > 1) {
        int64_t mid = lo + (hi - lo) / 2;
        if (twice(s, n, mid)) lo = mid;
        else hi = mid;
    }
    free(keys);
    free(heads);
    free(next_start);
    return lo;
}

static int64_t seed = 1062;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_word(int64_t n, int64_t k) {
    char *s = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = (char)('a' + next_random() % k);
    s[n] = 0;
    return s;
}

int main(void) {
    // 60 strings of 20000 letters over 2 to 26 of them, built once, then
    // each answered
    char *words[60];
    for (int w = 0; w < 60; w++) words[w] = random_word(20000, 2 + w % 25);
    int64_t calls = 0, total = 0, check = 0;
    for (int w = 0; w < 60; w++) {
        int64_t answer = longest_repeating(words[w]);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
        calls++;
    }
    printf("%lld calls: answers sum %lld, checksum %lld\n", (long long)calls, (long long)total,
           (long long)check);
    return 0;
}
