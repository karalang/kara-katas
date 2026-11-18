// LeetCode #1190 bench: the ★ arm in C, over the same 200 strings of about
// 2000 characters and 200 rounds as the Kāra bench.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    size_t len;
} Str;

static char *reverse_parentheses(const char *s, size_t n, size_t *out_len) {
    size_t *pair = malloc(n * sizeof(size_t) + 1);
    size_t *open = malloc(n * sizeof(size_t) + 1);
    size_t top = 0;
    for (size_t i = 0; i < n; i++) {
        if (s[i] == '(') {
            open[top++] = i;
        } else if (s[i] == ')') {
            size_t j = open[--top];
            pair[i] = j;
            pair[j] = i;
        }
    }
    char *out = malloc(n + 1);
    size_t len = 0;
    long i = 0, step = 1;
    while (i < (long)n) {
        char c = s[i];
        if (c == '(' || c == ')') {
            i = (long)pair[i];
            step = -step;
        } else {
            out[len++] = c;
        }
        i += step;
    }
    free(pair);
    free(open);
    *out_len = len;
    return out;
}

static long seed = 1190;

static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648L;
    return seed / 65536;
}

static const char LETTERS[] = "abcdefghijklmnopqrstuvwxyz";

static Str random_case(long n) {
    Str s = {malloc(2 * n + 1), 0};
    long open = 0;
    for (long k = 0; k < n; k++) {
        long r = next_random() % 4;
        if (r == 0) {
            s.data[s.len++] = '(';
            open++;
        } else if (r == 1 && open > 0) {
            s.data[s.len++] = ')';
            open--;
        } else {
            s.data[s.len++] = LETTERS[next_random() % 26];
        }
    }
    for (long k = 0; k < open; k++) {
        s.data[s.len++] = ')';
    }
    return s;
}

static Str nested(long depth) {
    Str s = {malloc(4 * depth + 1), 0};
    for (long k = 0; k < depth; k++) {
        s.data[s.len++] = LETTERS[next_random() % 26];
        s.data[s.len++] = '(';
    }
    for (long k = 0; k < depth; k++) {
        s.data[s.len++] = LETTERS[next_random() % 26];
        s.data[s.len++] = ')';
    }
    return s;
}

static long digest(const char *s, size_t n) {
    long h = 0;
    for (size_t i = 0; i < n; i++) {
        h = (h * 131 + (unsigned char)s[i]) % 1000000007;
    }
    return h;
}

int main(void) {
    Str cases[200];
    for (int i = 0; i < 200; i++) {
        cases[i] = i % 2 == 0 ? random_case(2000) : nested(500);
    }
    long check = 0;
    for (int r = 0; r < 200; r++) {
        for (int i = 0; i < 200; i++) {
            size_t len;
            char *out = reverse_parentheses(cases[i].data, cases[i].len, &len);
            check = (check * 131 + digest(out, len)) % 1000000007;
            free(out);
        }
    }
    printf("200 rounds of 200 strings of about 2000 characters: checksum %ld\n", check);
    for (int i = 0; i < 200; i++) {
        free(cases[i].data);
    }
    return 0;
}
