// LeetCode #953: Verifying an Alien Dictionary -- C mirror of the Kara
// bench program (a rank per letter).
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *s;
    long len;
} Word;

static bool is_alien_sorted(const Word *words, long n, const char *order) {
    long rank[26] = {0};
    for (long i = 0; i < 26; i++) {
        rank[order[i] - 'a'] = i;
    }
    for (long w = 1; w < n; w++) {
        const Word *a = &words[w - 1];
        const Word *b = &words[w];
        long k = 0;
        while (k < a->len && k < b->len && a->s[k] == b->s[k]) {
            k++;
        }
        if (k == b->len) {
            if (k < a->len) {
                return false;
            }
        } else if (k < a->len && rank[a->s[k] - 'a'] > rank[b->s[k] - 'a']) {
            return false;
        }
    }
    return true;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static bool before(const Word *a, const Word *b, const long *rank) {
    long k = 0;
    while (k < a->len && k < b->len && a->s[k] == b->s[k]) {
        k++;
    }
    if (k == b->len) {
        return false;
    } else if (k == a->len) {
        return true;
    }
    return rank[a->s[k] - 'a'] < rank[b->s[k] - 'a'];
}

int main(void) {
    const long rounds = 2000, count = 200, n = 100;
    long seed = 953;
    char (*orders)[27] = malloc(sizeof(char[27]) * count);
    Word **sets = malloc(sizeof(Word *) * count);
    for (long s = 0; s < count; s++) {
        char letters[26];
        for (long i = 0; i < 26; i++) {
            letters[i] = (char)('a' + i);
        }
        for (long i = 0; i < 26; i++) {
            long j = i + next_random(&seed) % (26 - i);
            char t = letters[i];
            letters[i] = letters[j];
            letters[j] = t;
        }
        long rank[26];
        for (long i = 0; i < 26; i++) {
            rank[letters[i] - 'a'] = i;
            orders[s][i] = letters[i];
        }
        orders[s][26] = 0;
        Word *words = malloc(sizeof(Word) * n);
        for (long i = 0; i < n; i++) {
            long m = 1 + next_random(&seed) % 20;
            words[i].s = malloc(m + 1);
            words[i].len = m;
            for (long c = 0; c < m; c++) {
                words[i].s[c] = letters[next_random(&seed) % 3];
            }
            words[i].s[m] = 0;
        }
        for (long i = 1; i < n; i++) {
            long j = i;
            while (j > 0 && before(&words[j], &words[j - 1], rank)) {
                Word t = words[j];
                words[j] = words[j - 1];
                words[j - 1] = t;
                j--;
            }
        }
        if (s % 3 == 2) {
            Word t = words[n - 2];
            words[n - 2] = words[n - 1];
            words[n - 1] = t;
        }
        sets[s] = words;
    }
    long sorted = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (long i = 0; i < count; i++) {
            long k = (r + i) % count;
            bool ok = is_alien_sorted(sets[k], n, orders[k]);
            if (ok) {
                sorted++;
            }
            check = (check * 31 + (ok ? 1 : 2)) % 1000000007;
        }
    }
    printf("%ld rounds over %ld sets of %ld words: %ld sorted, checksum %ld\n", rounds, count, n, sorted, check);
    return 0;
}
