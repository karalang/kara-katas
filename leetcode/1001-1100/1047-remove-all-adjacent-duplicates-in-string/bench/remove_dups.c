// LeetCode #1047: Remove All Adjacent Duplicates In String -- C mirror of
// bench/remove_dups.kara. C has no growable vector, so the stack is an array
// that doubles when full, as a Vec does. Its letters are 32-bit, as a Kāra
// or Rust `char` is, and the answer is encoded out of it into a string of its
// own, as `collect` does (one byte a letter, since every letter is ASCII).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static long long seed = 1047;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// the answer, malloc'd, and its length in *len
static char *remove_duplicates(const char *s, long long n, long long *len) {
    long long cap = 4, top = 0;
    uint32_t *stack = malloc(cap * sizeof(uint32_t));
    for (long long i = 0; i < n; i++) {
        uint32_t c = (unsigned char)s[i];
        if (top > 0 && stack[top - 1] == c) {
            top--;
        } else {
            if (top == cap) {
                cap *= 2;
                stack = realloc(stack, cap * sizeof(uint32_t));
            }
            stack[top++] = c;
        }
    }
    char *out = malloc(top + 1);
    for (long long i = 0; i < top; i++) out[i] = (char)stack[i];
    out[top] = 0;
    free(stack);
    *len = top;
    return out;
}

int main(void) {
    const int count = 100;
    const long long n = 200000;
    const int rounds = 10;
    char **strings = malloc(sizeof(char *) * count);
    for (int k = 0; k < count; k++) {
        strings[k] = malloc(n + 1);
        for (long long i = 0; i < n; i++) strings[k][i] = 'a' + next_random() % 4;
        strings[k][n] = 0;
    }
    long long total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            long long len;
            char *answer = remove_duplicates(strings[k], n, &len);
            long long last = len > 0 ? answer[len - 1] : 0;
            total += len;
            check = (check * 131 + len + last) % 1000000007;
            free(answer);
        }
    }
    printf("%d strings of %lld letters, %d rounds: total length %lld, checksum %lld\n", count, n, rounds, total, check);
    return 0;
}
