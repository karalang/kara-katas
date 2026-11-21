// LeetCode #2490: Circular Sentence -- C mirror of the ★ arm's benchmark
// (circular.kara): the same 200 sentences and 2300 passes, each letter
// changed and changed back, the sentence copied into a fresh buffer for
// every answer.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int is_circular_sentence(const char *s, int64_t n) {
    if (s[0] != s[n - 1]) return 0;
    for (int64_t i = 1; i < n - 1; i++) {
        if (s[i] == ' ' && s[i - 1] != s[i + 1]) return 0;
    }
    return 1;
}

static int64_t seed = 2490;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char letter(int64_t k) { return (char)('a' + k % 26); }

static char texts[200][512];
static int64_t lens[200];

static void sentence(int s) {
    char *text = texts[s];
    int64_t len = 0;
    char first = letter(next_random());
    char last = first;
    while (len < 490) {
        if (len > 0) text[len++] = ' ';
        text[len++] = last;
        int64_t extra = next_random() % 8;
        for (int64_t i = 0; i < extra; i++) text[len++] = letter(next_random());
        last = text[len - 1];
    }
    text[len++] = ' ';
    text[len++] = last;
    text[len++] = first;
    lens[s] = len;
}

int main(void) {
    const int64_t passes = 2300;
    for (int s = 0; s < 200; s++) sentence(s);
    static char buffer[512];
    int64_t check = 0, circular = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int s = 0; s < 200; s++) {
            int64_t n = lens[s];
            int64_t at = check % n;
            char was = texts[s][at];
            if (was != ' ') texts[s][at] = letter(check / n + p);
            memcpy(buffer, texts[s], (size_t)n);
            int answer = is_circular_sentence(buffer, n);
            texts[s][at] = was;
            if (answer) circular++;
            check = (check * 31 + (answer ? 1 : 2) + p) % 1000000007;
        }
    }
    printf("%lld passes over 200 sentences: %lld circular, checksum %lld\n", (long long)passes, (long long)circular, (long long)check);
    return 0;
}
