// LeetCode #1324 bench, C mirror of the Kāra bench: the ★ arm (the words
// split apart, row i made of each word's i-th letter or a space, the row's
// end trimmed) on 100 sentences of 200 letters and spaces built once; then
// 1000 passes, each setting one letter of every sentence from the checksum
// so far, answering it and folding the rows' letters plus the pass into the
// checksum. Each call takes fresh word and row arrays and a fresh buffer
// per row, a `malloc` each, as the Kāra arm takes a fresh `Vec` and
// `String`s.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char **rows;
    int64_t *lens;
    int64_t count;
} Rows;

static Rows print_vertically(const char *s, int64_t n) {
    int64_t words = 1;
    for (int64_t i = 0; i < n; i++)
        if (s[i] == ' ') words++;
    int64_t *start = malloc((size_t)words * sizeof(int64_t));
    int64_t *len = malloc((size_t)words * sizeof(int64_t));
    int64_t w = 0, tallest = 0;
    start[0] = 0;
    for (int64_t i = 0; i <= n; i++) {
        if (i == n || s[i] == ' ') {
            len[w] = i - start[w];
            if (len[w] > tallest) tallest = len[w];
            if (i < n) start[++w] = i + 1;
        }
    }
    Rows r;
    r.rows = malloc((size_t)tallest * sizeof(char *));
    r.lens = malloc((size_t)tallest * sizeof(int64_t));
    r.count = tallest;
    for (int64_t i = 0; i < tallest; i++) {
        char *row = malloc((size_t)words);
        for (int64_t j = 0; j < words; j++) row[j] = i < len[j] ? s[start[j] + i] : ' ';
        int64_t m = words;
        while (m > 0 && row[m - 1] == ' ') m--;
        r.rows[i] = row;
        r.lens[i] = m;
    }
    free(start);
    free(len);
    return r;
}

static int64_t seed = 1324;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 200;
    char sentences[100][200];
    for (int t = 0; t < 100; t++) {
        int64_t longest = t % 4 == 0 ? 3 : t % 4 == 1 ? 10 : t % 4 == 2 ? 40 : 200;
        int64_t m = 0;
        while (m < n) {
            int64_t len = 1 + next_random() % longest;
            for (int64_t k = 0; k < len; k++)
                if (m < n) sentences[t][m++] = (char)('A' + next_random() % 26);
            if (m < n - 1) sentences[t][m++] = ' ';
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 1000; pass++) {
        for (int t = 0; t < 100; t++) {
            int64_t at = check % n;
            if (sentences[t][at] != ' ') sentences[t][at] = (char)('A' + check / 7 % 26);
            Rows r = print_vertically(sentences[t], n);
            for (int64_t i = 0; i < r.count; i++) {
                for (int64_t k = 0; k < r.lens[i]; k++) check = (check * 131 + (unsigned char)r.rows[i][k]) % 1000000007;
                free(r.rows[i]);
            }
            check = (check * 31 + r.count + pass) % 1000000007;
            free(r.rows);
            free(r.lens);
        }
    }
    printf("1000 passes over 100 sentences of 200: checksum %lld\n", (long long)check);
    return 0;
}
