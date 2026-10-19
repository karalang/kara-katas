// LeetCode 806 — Number of Lines To Write String: the bench.
//
// 64 strings of 1000 letters, LeetCode's longest, each with widths of
// its own from 2 to 10, are made once; each round counts the lines of
// the next one.
#include <stdint.h>
#include <stdio.h>

static int64_t seed = 806;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void number_of_lines(const int64_t *widths, const char *s, int64_t *lines_out, int64_t *width_out) {
    int64_t lines = 1;
    int64_t width = 0;
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) {
        int64_t w = widths[*p - 97];
        if (width + w > 100) {
            lines += 1;
            width = w;
        } else {
            width += w;
        }
    }
    *lines_out = lines;
    *width_out = width;
}

static int64_t all_widths[64][26];
static char strings[64][1001];

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < 64; i++) {
        for (int j = 0; j < 26; j++) {
            all_widths[i][j] = 2 + next_random() % 9;
        }
        for (int j = 0; j < 1000; j++) {
            strings[i][j] = letters[next_random() % 26];
        }
        strings[i][1000] = 0;
    }
    int64_t rounds = 1000000;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t lines, width;
        number_of_lines(all_widths[r % 64], strings[r % 64], &lines, &width);
        total += lines;
        check = (check * 131 + lines * 1000 + width) % 1000000007;
    }
    printf("%lld rounds of 1000 letters: %lld lines in all, checksum %lld\n", (long long)rounds, (long long)total, (long long)check);
    return 0;
}
