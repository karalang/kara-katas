// Benchmark for #521: C mirror of the ★ arm (the whole longer word); see
// find_lus_length.kara. Words carry their lengths, as Kāra's strings do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *text;
    int64_t len;
} Word;

static int64_t find_lus_length(const Word *a, const Word *b) {
    if (a->len == b->len && memcmp(a->text, b->text, (size_t)a->len) == 0) return -1;
    return a->len > b->len ? a->len : b->len;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static Word random_word(int64_t *seed, int64_t len, int64_t letters) {
    Word w = {malloc(len + 2), len};
    for (int64_t i = 0; i < len; i++) w.text[i] = (char)(97 + next_random(seed) % letters);
    return w;
}

int main(void) {
    // 20,000 pairs of 1 to 100 letters from 1 to 3 letters made once (a
    // third equal, a third the first word with a letter added, a third
    // unrelated), then every pair answered in each of 5,000 rounds.
    int64_t seed = 521, n = 20000;
    Word *firsts = malloc(n * sizeof(Word)), *seconds = malloc(n * sizeof(Word));
    for (int64_t i = 0; i < n; i++) {
        int64_t letters = 1 + next_random(&seed) % 3;
        int64_t len = 1 + next_random(&seed) % 100;
        Word a = random_word(&seed, len, letters);
        Word b;
        if (i % 3 == 0) {
            b = (Word){malloc(a.len + 2), a.len};
            memcpy(b.text, a.text, (size_t)a.len);
        } else if (i % 3 == 1) {
            b = (Word){malloc(a.len + 2), a.len + 1};
            memcpy(b.text, a.text, (size_t)a.len);
            b.text[a.len] = (char)(97 + next_random(&seed) % letters);
        } else {
            int64_t blen = 1 + next_random(&seed) % 100;
            b = random_word(&seed, blen, letters);
        }
        firsts[i] = a;
        seconds[i] = b;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < 5000; round++)
        for (int64_t i = 0; i < n; i++) {
            int64_t k = find_lus_length(&firsts[i], &seconds[i]);
            total += k;
            checksum = (checksum + (round + 1) * (k + 2)) % 1000000007;
        }
    printf("20000 pairs, 5000 rounds: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    for (int64_t i = 0; i < n; i++) {
        free(firsts[i].text);
        free(seconds[i].text);
    }
    free(firsts);
    free(seconds);
    return 0;
}
