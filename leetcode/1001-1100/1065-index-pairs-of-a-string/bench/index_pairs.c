// LeetCode #1065: Index Pairs of a String -- the benchmark, the same
// every-start-against-every-word search as index_pairs.kara, with the
// pairs in a growable array sorted by qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t i, j;
} Pair;

typedef struct {
    Pair *at;
    int64_t len, cap;
} Pairs;

static int by_pair(const void *a, const void *b) {
    const Pair *p = a, *q = b;
    if (p->i != q->i) return p->i < q->i ? -1 : 1;
    if (p->j != q->j) return p->j < q->j ? -1 : 1;
    return 0;
}

static Pairs index_pairs(const char *text, int64_t n, char **words, int64_t *lens, int64_t count) {
    Pairs pairs = {malloc(4 * sizeof(Pair)), 0, 4};
    for (int64_t i = 0; i < n; i++) {
        for (int64_t w = 0; w < count; w++) {
            if (lens[w] <= n - i && memcmp(text + i, words[w], lens[w]) == 0) {
                if (pairs.len == pairs.cap) {
                    pairs.cap *= 2;
                    pairs.at = realloc(pairs.at, pairs.cap * sizeof(Pair));
                }
                pairs.at[pairs.len++] = (Pair){i, i + lens[w] - 1};
            }
        }
    }
    qsort(pairs.at, pairs.len, sizeof(Pair), by_pair);
    return pairs;
}

static int64_t seed = 1065;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *random_word(int64_t n, int64_t k) {
    char *s = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = 'a' + next_random() % k;
    s[n] = 0;
    return s;
}

// Up to `count` distinct words of 1 to `longest` letters over `k`: each
// drawn at random or, every other one, cut from the text.
static int64_t random_words(const char *text, int64_t len, int64_t count, int64_t longest, int64_t k,
                            char **words) {
    int64_t have = 0;
    for (int64_t w = 0; w < count; w++) {
        int64_t n = next_random() % longest + 1;
        char *word;
        if (w % 2 == 1 && n <= len) {
            int64_t at = next_random() % (len - n + 1);
            word = malloc(n + 1);
            memcpy(word, text + at, n);
            word[n] = 0;
        } else {
            word = random_word(n, k);
        }
        int seen = 0;
        for (int64_t v = 0; v < have; v++) seen |= strcmp(words[v], word) == 0;
        if (seen)
            free(word);
        else
            words[have++] = word;
    }
    return have;
}

int main(void) {
    // 40 texts of 20000 letters over 2 to 4, each with up to 100 words of 1
    // to 12 letters, built once, then each answered
    char *texts[40];
    char *lists[40][100];
    int64_t lens[40][100], counts[40];
    for (int64_t t = 0; t < 40; t++) {
        int64_t k = 2 + t % 3;
        texts[t] = random_word(20000, k);
        counts[t] = random_words(texts[t], 20000, 100, 12, k, lists[t]);
        for (int64_t w = 0; w < counts[t]; w++) lens[t][w] = strlen(lists[t][w]);
    }
    int64_t calls = 0, count = 0, check = 0;
    for (int t = 0; t < 40; t++) {
        Pairs pairs = index_pairs(texts[t], 20000, lists[t], lens[t], counts[t]);
        count += pairs.len;
        for (int64_t p = 0; p < pairs.len; p++)
            check = (check * 31 + pairs.at[p].i * 101 + pairs.at[p].j + 1) % 1000000007;
        free(pairs.at);
        calls++;
    }
    printf("%lld calls: %lld pairs, checksum %lld\n", (long long)calls, (long long)count,
           (long long)check);
    return 0;
}
