// LeetCode #1618: Maximum Font to Fit a Sentence in a Screen -- the bench in
// C, mirroring fonts.kara: a binary search for the last size that fits.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int32_t base[26];
} Font;

static int32_t get_width(const Font *f, int32_t font_size, char ch) {
    return (font_size * f->base[ch - 'a'] + 3) / 4;
}

static int32_t get_height(const Font *f, int32_t font_size) {
    (void)f;
    return font_size + font_size / 4;
}

static int fits(const char *text, int64_t n, int32_t w, int32_t h, int32_t size, const Font *info) {
    if (get_height(info, size) > h) return 0;
    int64_t sum = 0;
    for (int64_t i = 0; i < n; i++) sum += get_width(info, size, text[i]);
    return sum <= w;
}

static int32_t max_font(const char *text, int64_t n, int32_t w, int32_t h, const int32_t *fonts,
                        int64_t m, const Font *info) {
    int64_t lo = 0, hi = m;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (fits(text, n, w, h, fonts[mid], info)) lo = mid + 1;
        else hi = mid;
    }
    return lo == 0 ? -1 : fonts[lo - 1];
}

static int64_t seed = 1618;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { TEXTS = 200, LEN = 5000 };
    char *texts = malloc((size_t)TEXTS * LEN);
    for (int t = 0; t < TEXTS; t++)
        for (int i = 0; i < LEN; i++) texts[(size_t)t * LEN + i] = (char)('a' + next_random() % 26);
    Font font;
    for (int k = 0; k < 26; k++) font.base[k] = (int32_t)(next_random() % 8 + 1);
    int32_t fonts[60];
    for (int k = 0; k < 60; k++) fonts[k] = (k + 1) * 3;
    int64_t check = 0, total = 0;
    for (int t = 0; t < TEXTS; t++) {
        for (int q = 0; q < 40; q++) {
            int32_t w = (int32_t)(next_random() * 8 + 1);
            int32_t h = (int32_t)(next_random() % 240 + 1);
            int32_t answer = max_font(texts + (size_t)t * LEN, LEN, w, h, fonts, 60, &font);
            check = (check * 31 + answer + 1) % 1000000007;
            total += answer;
        }
    }
    printf("8000 screens of 5000 letters: sizes total %lld, checksum %lld\n", (long long)total,
           (long long)check);
    free(texts);
    return 0;
}
