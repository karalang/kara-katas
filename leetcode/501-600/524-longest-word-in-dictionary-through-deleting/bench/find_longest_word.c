// Benchmark for #524: C mirror of the ★ arm (check every word); see
// find_longest_word.kara. Each word keeps its length beside its letters,
// as Kāra's strings do. Like the ★ arm, every subsequence test copies the
// word's letters into a fresh array, and a new best word is copied.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *p;
    int64_t len;
} Str;

static int64_t seed;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int is_subsequence(Str word, Str s) {
    char *w = malloc(word.len > 0 ? word.len : 1);
    memcpy(w, word.p, word.len);
    int64_t i = 0;
    for (int64_t j = 0; j < s.len; j++) {
        if (i < word.len && w[i] == s.p[j]) i++;
    }
    free(w);
    return i == word.len;
}

static Str find_longest_word(Str s, Str *dictionary, int64_t count) {
    Str best = {malloc(1), 0};
    for (int64_t k = 0; k < count; k++) {
        Str word = dictionary[k];
        if (word.len > best.len || (word.len == best.len && memcmp(word.p, best.p, word.len) < 0)) {
            if (is_subsequence(word, s)) {
                free(best.p);
                best.p = malloc(word.len);
                memcpy(best.p, word.p, word.len);
                best.len = word.len;
            }
        }
    }
    return best;
}

static Str random_word(int64_t len, int64_t letters) {
    Str w = {malloc(len > 0 ? len : 1), len};
    for (int64_t i = 0; i < len; i++) w.p[i] = (char)(97 + next_random() % letters);
    return w;
}

static Str random_subsequence(Str s, int64_t keep) {
    Str w = {malloc(s.len), 0};
    for (int64_t i = 0; i < s.len; i++) {
        if (next_random() % keep == 0) w.p[w.len++] = s.p[i];
    }
    if (w.len == 0) w.p[w.len++] = s.p[0];
    return w;
}

int main(void) {
    seed = 524;
    Str texts[20];
    Str *dictionaries[20];
    for (int c = 0; c < 20; c++) {
        int64_t letters = 2 + next_random() % 4;
        texts[c] = random_word(1000, letters);
        dictionaries[c] = malloc(1000 * sizeof(Str));
        for (int i = 0; i < 1000; i++) {
            if (next_random() % 3 == 0) {
                int64_t keep = 2 + next_random() % 30;
                dictionaries[c][i] = random_subsequence(texts[c], keep);
            } else {
                int64_t len = 1 + next_random() % 1000;
                dictionaries[c][i] = random_word(len, letters);
            }
        }
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < 20; r++) {
        for (int c = 0; c < 20; c++) {
            Str answer = find_longest_word(texts[c], dictionaries[c], 1000);
            total += answer.len;
            for (int64_t i = 0; i < answer.len; i++)
                checksum = (checksum * 31 + (unsigned char)answer.p[i]) % 1000000007;
            free(answer.p);
        }
    }
    printf("20 cases, 20 rounds: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
