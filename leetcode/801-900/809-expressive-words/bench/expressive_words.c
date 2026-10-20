// LeetCode 809 -- Expressive Words: the bench, with the ★ arm's two
// pointers over the groups.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t seed = 809;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static bool stretchy(const char *a, int64_t na, const char *b, int64_t nb) {
    int64_t i = 0, j = 0;
    while (i < na && j < nb) {
        char c = a[i];
        if (b[j] != c) return false;
        int64_t from_i = i;
        while (i < na && a[i] == c) i++;
        int64_t from_j = j;
        while (j < nb && b[j] == c) j++;
        int64_t in_s = i - from_i, in_word = j - from_j;
        if (in_s < in_word || (in_s > in_word && in_s < 3)) return false;
    }
    return i == na && j == nb;
}

static char texts[64][128];
static int64_t text_len[64];
static char words[64][100][128];
static int64_t word_len[64][100];

static int64_t expressive_words(int64_t k) {
    int64_t count = 0;
    for (int w = 0; w < 100; w++)
        if (stretchy(texts[k], text_len[k], words[k][w], word_len[k][w])) count++;
    return count;
}

static int64_t spell(char *out, const char *cs, const int64_t *ns) {
    int64_t len = 0;
    for (int g = 0; g < 25; g++)
        for (int64_t k = 0; k < ns[g]; k++) out[len++] = cs[g];
    return len;
}

int main(void) {
    for (int k = 0; k < 64; k++) {
        char cs[25];
        int64_t ns[25];
        int64_t last = 26;
        for (int g = 0; g < 25; g++) {
            int64_t c = next_random() % 5;
            if (c == last) c = (c + 1) % 5;
            last = c;
            cs[g] = (char)(97 + c);
            ns[g] = 1 + next_random() % 4;
        }
        for (int w = 0; w < 100; w++) {
            if (next_random() % 4 == 0) {
                int64_t n = 1 + next_random() % 100;
                for (int64_t i = 0; i < n; i++) words[k][w][i] = (char)(97 + next_random() % 5);
                word_len[k][w] = n;
            } else {
                int64_t shrunk[25];
                for (int g = 0; g < 25; g++) shrunk[g] = ns[g] >= 3 ? 1 + next_random() % ns[g] : ns[g];
                if (next_random() % 3 == 0) {
                    int64_t g = next_random() % 25;
                    shrunk[g] = ns[g] + 1;
                }
                word_len[k][w] = spell(words[k][w], cs, shrunk);
            }
        }
        text_len[k] = spell(texts[k], cs, ns);
    }
    int64_t rounds = 200000, total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t n = expressive_words(r % 64);
        total += n;
        check = (check * 131 + n + r) % 1000000007;
    }
    printf("%lld rounds of 100 words: %lld stretchy, checksum %lld\n", (long long)rounds, (long long)total, (long long)check);
    return 0;
}
