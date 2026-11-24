// LeetCode #1320 bench, C mirror of the Kāra bench: the ★ arm (one row of
// 27 for the other finger's key, carried from letter to letter) on 100
// words of 300 letters over 2, 5 or 26 letters, built once; then 80
// passes, each setting one letter of every word from the checksum so far,
// answering it and folding the answer plus the pass into the checksum.
// Each call takes a fresh row for every letter, a `malloc`, as the Kāra arm
// takes a fresh `Vec`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t iabs(int64_t x) { return x < 0 ? -x : x; }

static int64_t key_distance(int64_t a, int64_t b) {
    if (a == 26) return 0;
    return iabs(a / 6 - b / 6) + iabs(a % 6 - b % 6);
}

static int64_t minimum_distance(const char *word, int64_t n) {
    int64_t *w = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) w[i] = (int64_t)(unsigned char)word[i] - 65;
    const int64_t far = 1000000;
    int64_t *other = malloc(27 * sizeof(int64_t));
    for (int j = 0; j < 27; j++) other[j] = far;
    other[26] = 0;
    for (int64_t i = 1; i < n; i++) {
        int64_t last = w[i - 1], now = w[i];
        int64_t *next = malloc(27 * sizeof(int64_t));
        for (int j = 0; j < 27; j++) next[j] = far;
        for (int64_t j = 0; j < 27; j++) {
            if (other[j] < far) {
                int64_t a = other[j] + key_distance(last, now);
                if (a < next[j]) next[j] = a;
                int64_t b = other[j] + key_distance(j, now);
                if (b < next[last]) next[last] = b;
            }
        }
        free(other);
        other = next;
    }
    int64_t best = other[0];
    for (int j = 1; j < 27; j++)
        if (other[j] < best) best = other[j];
    free(other);
    free(w);
    return best;
}

static int64_t seed = 1320;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    static char words[100][301];
    for (int t = 0; t < 100; t++) {
        int64_t k = t % 3 == 0 ? 2 : t % 3 == 1 ? 5 : 26;
        int64_t base = next_random() % (27 - k);
        for (int i = 0; i < 300; i++) words[t][i] = letters[base + next_random() % k];
        words[t][300] = 0;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 80; pass++) {
        for (int t = 0; t < 100; t++) {
            words[t][check % 300] = letters[(check / 7) % 26];
            int64_t got = minimum_distance(words[t], 300);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("80 passes over 100 words of 300: checksum %lld\n", (long long)check);
    return 0;
}
