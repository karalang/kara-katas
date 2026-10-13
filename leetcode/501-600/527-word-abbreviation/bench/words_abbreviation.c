// Benchmark for #527: C mirror of the ★ arm (grow clashing prefixes); see
// words_abbreviation.kara. Like the ★ arm, every abbreviation is a fresh
// heap string; the list of clashing words is one buffer per call rather
// than a fresh vector per round. Words keep their lengths beside their
// letters, as Kāra's strings do. While the lists are made, a repeated
// word is found by a linear scan, where the others use a hash set.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *p;
    int64_t len;
} Str;

static Str abbreviate(Str word, int64_t k) {
    int64_t n = word.len;
    Str out;
    if (k >= n - 2) {
        out.p = malloc(n);
        memcpy(out.p, word.p, n);
        out.len = n;
        return out;
    }
    char buf[32];
    int digits = snprintf(buf, sizeof buf, "%lld", (long long)(n - 1 - k));
    out.len = k + digits + 1;
    out.p = malloc(out.len);
    memcpy(out.p, word.p, k);
    memcpy(out.p + k, buf, digits);
    out.p[out.len - 1] = word.p[n - 1];
    return out;
}

static int same(Str a, Str b) { return a.len == b.len && memcmp(a.p, b.p, a.len) == 0; }

static Str *words_abbreviation(Str *words, int64_t n) {
    int64_t *prefix = malloc(n * sizeof(int64_t));
    Str *abbr = malloc(n * sizeof(Str));
    int64_t *clash = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        prefix[i] = 1;
        abbr[i] = abbreviate(words[i], 1);
    }
    for (int64_t i = 0; i < n; i++) {
        for (;;) {
            int64_t m = 0;
            for (int64_t j = i + 1; j < n; j++)
                if (same(abbr[j], abbr[i])) clash[m++] = j;
            if (m == 0) break;
            clash[m++] = i;
            for (int64_t c = 0; c < m; c++) {
                int64_t j = clash[c];
                prefix[j]++;
                free(abbr[j].p);
                abbr[j] = abbreviate(words[j], prefix[j]);
            }
        }
    }
    free(prefix);
    free(clash);
    return abbr;
}

static int64_t seed = 527;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static Str random_word(int64_t len, int64_t letters) {
    Str w = {malloc(len), len};
    for (int64_t i = 0; i < len; i++) w.p[i] = (char)(97 + next_random() % letters);
    return w;
}

int main(void) {
    Str *lists[20];
    for (int l = 0; l < 20; l++) {
        lists[l] = malloc(400 * sizeof(Str));
        int64_t count = 0;
        while (count < 400) {
            int64_t len = 8 + next_random() % 9;
            Str word = random_word(len, 2);
            int seen = 0;
            for (int64_t i = 0; i < count && !seen; i++) seen = same(lists[l][i], word);
            if (seen) {
                free(word.p);
            } else {
                lists[l][count++] = word;
            }
        }
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < 50; r++) {
        for (int l = 0; l < 20; l++) {
            Str *abbr = words_abbreviation(lists[l], 400);
            for (int i = 0; i < 400; i++) {
                total += abbr[i].len;
                for (int64_t k = 0; k < abbr[i].len; k++)
                    checksum = (checksum * 31 + (unsigned char)abbr[i].p[k]) % 1000000007;
                free(abbr[i].p);
            }
            free(abbr);
        }
    }
    printf("20 lists of 400 words, 50 rounds: %lld letters, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
