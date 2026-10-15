// Benchmark for #676: every word of the same length compared, as the
// Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 676;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    char **words;
    int64_t count;
} MagicDictionary;

static void build_dict(MagicDictionary *d, char **dictionary, int64_t count) {
    d->words = malloc(sizeof(char *) * count);
    for (int64_t i = 0; i < count; i++) d->words[i] = strdup(dictionary[i]);
    d->count = count;
}

static int search(const MagicDictionary *d, const char *search_word) {
    size_t n = strlen(search_word);
    for (int64_t k = 0; k < d->count; k++) {
        const char *a = d->words[k];
        if (strlen(a) == n) {
            int64_t diff = 0;
            for (size_t i = 0; i < n; i++) {
                if (a[i] != search_word[i]) diff += 1;
            }
            if (diff == 1) return 1;
        }
    }
    return 0;
}

static void free_dict(MagicDictionary *d) {
    for (int64_t i = 0; i < d->count; i++) free(d->words[i]);
    free(d->words);
}

static char *random_word(int64_t length) {
    char *s = malloc(length + 1);
    for (int64_t i = 0; i < length; i++) s[i] = (char)(97 + next_random() % 2);
    s[length] = 0;
    return s;
}

int main(void) {
    int64_t rounds = 1000;
    int64_t sum = 0;
    int64_t found = 0;
    char *dictionary[100];
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 100; i++) dictionary[i] = random_word(50);
        MagicDictionary d;
        build_dict(&d, dictionary, 100);
        for (int64_t k = 0; k < 100; k++) {
            char *word;
            if (k % 2 == 0) {
                word = strdup(dictionary[next_random() % 100]);
                int64_t at = next_random() % 50;
                word[at] = word[at] == 'a' ? 'b' : 'a';
            } else {
                word = random_word(50);
            }
            if (search(&d, word)) {
                found += 1;
                sum = (sum * 3 + 1) % 1000000007;
            } else {
                sum = sum * 3 % 1000000007;
            }
            free(word);
        }
        free_dict(&d);
        for (int64_t i = 0; i < 100; i++) free(dictionary[i]);
    }
    printf("%lld dictionaries of 100 words, %lld searches, %lld found: checksum %lld\n",
           (long long)rounds, (long long)(rounds * 100), (long long)found, (long long)sum);
    return 0;
}
