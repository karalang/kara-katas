// LeetCode #1750: Minimum Length of String After Deleting Similar Ends --
// the bench (ends.kara in C): two pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { COUNT = 50, ROUNDS = 40, N = 100000 };

static int32_t minimum_length(const char *b, int64_t len) {
    int64_t left = 0, right = len - 1;
    while (left < right && b[left] == b[right]) {
        char c = b[left];
        while (left <= right && b[left] == c) left++;
        while (right >= left && b[right] == c) right--;
    }
    return (int32_t)(right - left + 1);
}

static int64_t seed = 1750;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// a random middle of up to 1000 letters from `a` and `b`, wrapped in
// layers of one letter on both sides until the string is `n` long; the
// front layers are kept as (letter, count) and written back to front
static char *draw(int64_t n, int64_t *len) {
    char middle[1000];
    int64_t m = next_random() % 1000;
    for (int64_t i = 0; i < m; i++) middle[i] = (char)('a' + next_random() % 2);
    int64_t cap = n + 8;
    char *front_letter = malloc(cap), *back = malloc(cap);
    int64_t *front_count = malloc(cap * sizeof(int64_t));
    int64_t layers = 0, back_len = 0, size = m;
    while (size < n) {
        char letter = (char)('a' + next_random() % 2);
        int64_t before = next_random() % 3 + 1;
        int64_t after = next_random() % 3 + 1;
        front_letter[layers] = letter;
        front_count[layers++] = before;
        for (int64_t i = 0; i < after; i++) back[back_len++] = letter;
        size += before + after;
    }
    char *s = malloc(size + 1);
    int64_t at = 0;
    for (int64_t l = layers - 1; l >= 0; l--)
        for (int64_t i = 0; i < front_count[l]; i++) s[at++] = front_letter[l];
    memcpy(s + at, middle, m);
    at += m;
    memcpy(s + at, back, back_len);
    at += back_len;
    s[at] = 0;
    free(front_letter);
    free(back);
    free(front_count);
    *len = at;
    return s;
}

int main(void) {
    char *strings[COUNT];
    int64_t lens[COUNT];
    for (int c = 0; c < COUNT; c++) strings[c] = draw(N, &lens[c]);
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = minimum_length(strings[c], lens[c]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d strings of about %d letters, %d rounds: lengths add to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)sum, (long long)check);
    for (int c = 0; c < COUNT; c++) free(strings[c]);
    return 0;
}
