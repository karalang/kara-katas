// LeetCode #1021: Remove Outermost Parentheses -- bench
// Mirrors ./remove_outer.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char *data;
    int64_t len, cap;
} Str;

static void push(Str *s, char c) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 8;
        s->data = realloc(s->data, s->cap);
    }
    s->data[s->len++] = c;
}

static Str remove_outer_parentheses(const Str *s) {
    Str out = {0};
    int64_t depth = 0;
    for (int64_t i = 0; i < s->len; i++) {
        char c = s->data[i];
        if (c == '(') {
            if (depth > 0) push(&out, c);
            depth += 1;
        } else {
            depth -= 1;
            if (depth > 0) push(&out, c);
        }
    }
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 100, rounds = 30;
    int64_t seed = 1021, chars = 0;
    Str *strings = calloc(count, sizeof *strings);
    for (int64_t g = 0; g < count; g++) {
        int64_t pairs = (next_random(&seed) * 32768 + next_random(&seed)) % 50000 + 1;
        int64_t open = 2 + next_random(&seed) % 5;
        int64_t left = pairs, depth = 0;
        while (left > 0 || depth > 0) {
            int opens = depth == 0 ? 1 : left == 0 ? 0 : next_random(&seed) % 8 < open;
            if (opens) {
                push(&strings[g], '(');
                left -= 1;
                depth += 1;
            } else {
                push(&strings[g], ')');
                depth -= 1;
            }
        }
        chars += strings[g].len;
    }
    int64_t kept = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < count; g++) {
            Str answer = remove_outer_parentheses(&strings[g]);
            int64_t n = answer.len;
            int64_t middle = n > 0 ? (unsigned char)answer.data[n / 2] : 0;
            kept += n;
            check = (check * 31 + n * 2 + middle) % 1000000007;
            free(answer.data);
        }
    }
    printf("%lld strings, %lld characters, %lld rounds: %lld kept, checksum %lld\n", (long long)count,
           (long long)chars, (long long)rounds, (long long)kept, (long long)check);
    return 0;
}
