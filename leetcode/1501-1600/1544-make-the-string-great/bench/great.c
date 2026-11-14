// LeetCode #1544: Make The String Great -- bench: the ★ arm (a stack) over
// 1000 strings of 1 to 100 letters (the constraint's bound), each over its
// own first 1 to 3 letters in both cases, built once, each made great 500
// times. C mirror of great.kara: the stack is a fresh heap buffer per call,
// as the Kāra arm's Vec and String are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char lower(char c) { return (c >= 'A' && c <= 'Z') ? (char)(c | 32) : c; }

static char *make_good(const char *s, int64_t n, int64_t *len) {
    char *stack = malloc(n + 1);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        char c = s[i];
        if (top > 0 && stack[top - 1] != c && lower(stack[top - 1]) == lower(c)) {
            top -= 1;
        } else {
            stack[top++] = c;
        }
    }
    stack[top] = 0;
    *len = top;
    return stack;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1544;
    char *strings[1000];
    int64_t lens[1000];
    for (int k = 0; k < 1000; k++) {
        int64_t n = next_random(&seed) % 100 + 1;
        int64_t used = next_random(&seed) % 3 + 1;
        char *s = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) {
            char base = next_random(&seed) % 2 == 0 ? 'a' : 'A';
            s[i] = (char)(base + next_random(&seed) % used);
        }
        s[n] = 0;
        strings[k] = s;
        lens[k] = n;
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < 500; p++) {
        for (int k = 0; k < 1000; k++) {
            int64_t len;
            char *great = make_good(strings[k], lens[k], &len);
            total += len;
            check = mix(check, len);
            free(great);
        }
    }
    for (int k = 0; k < 1000; k++) free(strings[k]);
    printf("500 passes over 1000 strings of up to 100 letters: %lld letters kept, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
