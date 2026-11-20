// LeetCode #2390: Removing Stars From a String -- the bench, the ★ arm in
// C: a stack, a letter pushed and a star popping.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2390;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *starred(int64_t len, int64_t odds) {
    char *out = malloc(len + 1);
    int64_t depth = 0;
    for (int64_t i = 0; i < len; i++) {
        if (depth > 0 && next_random() % odds == 0) {
            out[i] = '*';
            depth--;
        } else {
            out[i] = (char)('a' + next_random() % 26);
            depth++;
        }
    }
    out[len] = 0;
    return out;
}

// The answer in a fresh buffer, its length through *len.
static char *remove_stars(const char *s, int64_t n, int64_t *len) {
    char *stack = malloc(n + 1);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == '*') {
            if (top > 0) top--;
        } else {
            stack[top++] = s[i];
        }
    }
    stack[top] = 0;
    *len = top;
    return stack;
}

int main(void) {
    char *strings[20];
    for (int i = 0; i < 20; i++) strings[i] = starred(100000, 3);
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++) {
        for (int i = 0; i < 20; i++) {
            int64_t len;
            char *t = remove_stars(strings[i], 100000, &len);
            for (int64_t j = 0; j < len; j++) check = (check * 31 + (t[j] - 'a' + 1)) % 1000000007;
            check = (check * 31 + len + p) % 1000000007;
            free(t);
        }
    }
    printf("100 passes over 20 strings of 10^5 characters: checksum %lld\n", (long long)check);
    for (int i = 0; i < 20; i++) free(strings[i]);
    return 0;
}
