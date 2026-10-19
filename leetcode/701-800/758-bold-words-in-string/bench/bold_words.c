// LeetCode 758 — Bold Words in String: benchmark, the ★ arm in C.
// Occurrences are found with strstr, searching again from one past each.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *bold_words(char words[][11], int count, const char *s) {
    size_t n = strlen(s);
    bool *bold = calloc(n, sizeof(bool));
    for (int w = 0; w < count; w++) {
        size_t len = strlen(words[w]);
        size_t from = 0;
        while (from < n) {
            const char *hit = strstr(s + from, words[w]);
            if (!hit) break;
            size_t at = (size_t)(hit - s);
            for (size_t i = at; i < at + len; i++) bold[i] = true;
            from = at + 1;
        }
    }
    char *out = malloc(n * 8 + 1);
    size_t k = 0;
    for (size_t i = 0; i < n; i++) {
        if (bold[i] && (i == 0 || !bold[i - 1])) {
            memcpy(out + k, "<b>", 3);
            k += 3;
        }
        out[k++] = s[i];
        if (bold[i] && (i == n - 1 || !bold[i + 1])) {
            memcpy(out + k, "</b>", 4);
            k += 4;
        }
    }
    out[k] = 0;
    free(bold);
    return out;
}

static int64_t seed = 758;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_text(char *text, int64_t length, int64_t letters) {
    for (int64_t i = 0; i < length; i++) text[i] = (char)('a' + next_random() % letters);
    text[length] = 0;
}

int main(void) {
    int64_t rounds = 20000, total = 0, check = 0;
    char s[501];
    char words[50][11];
    for (int64_t r = 0; r < rounds; r++) {
        random_text(s, 500, 4);
        for (int w = 0; w < 50; w++) {
            int64_t size = 1 + next_random() % 10;
            random_text(words[w], size, 5);
        }
        char *answer = bold_words(words, 50, s);
        size_t len = strlen(answer);
        total += (int64_t)len;
        for (size_t i = 0; i < len; i++) check = (check * 31 + (unsigned char)answer[i]) % 1000000007;
        free(answer);
    }
    printf("%lld strings of 500 letters: %lld characters out, checksum %lld\n", (long long)rounds,
           (long long)total, (long long)check);
    return 0;
}
