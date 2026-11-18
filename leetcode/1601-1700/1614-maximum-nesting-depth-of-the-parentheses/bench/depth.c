// LeetCode #1614: Maximum Nesting Depth of the Parentheses -- the bench in
// C, mirroring depth.kara: one pass counting the parentheses open, keeping
// the most.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *buf;
    int64_t len, cap;
} Str;

static void push(Str *s, char c) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 64;
        s->buf = realloc(s->buf, s->cap);
    }
    s->buf[s->len++] = c;
}

static int32_t max_depth(const char *s, int64_t n) {
    int32_t open = 0, most = 0;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == '(') {
            open++;
            if (open > most) most = open;
        } else if (s[i] == ')') {
            open--;
        }
    }
    return most;
}

static int64_t seed = 1614;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void expression(int64_t size, Str *out) {
    int64_t left = size;
    for (;;) {
        if (left > 1 && next_random() % 3 == 0) {
            int64_t inner = next_random() % left + 1;
            push(out, '(');
            expression(inner, out);
            push(out, ')');
            left -= inner;
        } else {
            push(out, (char)('0' + next_random() % 10));
            left -= 1;
        }
        if (left <= 0) break;
        push(out, "+-*/"[next_random() % 4]);
    }
}

int main(void) {
    Str expressions[10];
    memset(expressions, 0, sizeof expressions);
    for (int e = 0; e < 10; e++) expression(200000, &expressions[e]);
    int64_t check = 0, chars = 0;
    for (int e = 0; e < 10; e++) {
        for (int k = 0; k < 10; k++) {
            check = (check * 31 + max_depth(expressions[e].buf, expressions[e].len) + 1) % 1000000007;
            chars += expressions[e].len;
        }
    }
    printf("10 expressions of 200000 terms, each read 10 times: %lld characters, checksum %lld\n",
           (long long)chars, (long long)check);
    for (int e = 0; e < 10; e++) free(expressions[e].buf);
    return 0;
}
