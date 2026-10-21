// Benchmark for #824: Goat Latin -- the ★ arm (split, growing suffix).
//
// Mirrors goat_latin.kara: the sentence split at spaces, each word keeping
// a first vowel and moving a first consonant to the end, then "ma" and a
// run of 'a's kept in a buffer that grows by one letter per word. The
// answer is a fresh growable buffer, as the Kāra program's String is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    int64_t len;
    int64_t cap;
} Buf;

static void buf_reserve(Buf *b, int64_t extra) {
    if (b->len + extra > b->cap) {
        int64_t cap = b->cap ? b->cap * 2 : 8;
        while (cap < b->len + extra) cap *= 2;
        b->data = realloc(b->data, (size_t)cap);
        b->cap = cap;
    }
}

static void buf_push(Buf *b, char c) {
    buf_reserve(b, 1);
    b->data[b->len++] = c;
}

static void buf_push_str(Buf *b, const char *s, int64_t n) {
    buf_reserve(b, n);
    memcpy(b->data + b->len, s, (size_t)n);
    b->len += n;
}

static int is_vowel(char c) { return strchr("aeiouAEIOU", c) != NULL; }

static Buf to_goat_latin(const char *s, int64_t n) {
    Buf answer = {0};
    Buf tail = {0};
    int64_t start = 0;
    while (start <= n) {
        int64_t end = start;
        while (end < n && s[end] != ' ') end++;
        buf_push(&tail, 'a');
        if (answer.len > 0) buf_push(&answer, ' ');
        char first = s[start];
        if (is_vowel(first)) {
            buf_push_str(&answer, s + start, end - start);
        } else {
            buf_push_str(&answer, s + start + 1, end - start - 1);
            buf_push(&answer, first);
        }
        buf_push_str(&answer, "ma", 2);
        buf_push_str(&answer, tail.data, tail.len);
        start = end + 1;
    }
    free(tail.data);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 64;
    int64_t rounds = 2000000;
    const char *letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int64_t seed = 824;
    char sentences[64][151];
    int64_t lengths[64];
    for (int64_t g = 0; g < count; g++) {
        int64_t len = 0;
        for (;;) {
            int64_t length = 1 + next_random(&seed) % 9;
            int64_t extra = len == 0 ? length : length + 1;
            if (len + extra > 150) break;
            if (len > 0) sentences[g][len++] = ' ';
            for (int64_t i = 0; i < length; i++) sentences[g][len++] = letters[next_random(&seed) % 52];
        }
        sentences[g][len] = '\0';
        lengths[g] = len;
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        Buf answer = to_goat_latin(sentences[g], lengths[g]);
        total += answer.len;
        checksum = (checksum * 131 + (unsigned char)answer.data[round % answer.len]) % 1000000007;
        free(answer.data);
    }
    printf("%lld rounds of %lld sentences: total %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
