// Bench mirror of backtracking.kara — same owned-snapshot recursive
// backtracking (each child call gets a freshly malloc'd copy of the
// prefix plus one appended bracket), same K x n=10 full-set generation,
// same total-bytes sink. Strings are materialized into a growing
// pointer array and fully freed each iteration, matching the per-iter
// allocator traffic of the Kara/Rust/Go mirrors.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    char **data;
    size_t len;
    size_t cap;
} StrVec;

static void sv_push(StrVec *v, char *s) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(char *));
    }
    v->data[v->len++] = s;
}

// cur is an owned heap string of length cur_len (NUL-terminated).
// The base case moves it into the output array; the recursive arms
// build extended copies — the same immutable-snapshot shape as the
// Kara mirror's f-string concat.
static void backtrack(char *cur, size_t cur_len, long open, long close, long n, StrVec *out) {
    if (close == n) {
        sv_push(out, cur);
        return;
    }
    if (open < n) {
        char *child = malloc(cur_len + 2);
        memcpy(child, cur, cur_len);
        child[cur_len] = '(';
        child[cur_len + 1] = '\0';
        backtrack(child, cur_len + 1, open + 1, close, n, out);
    }
    if (close < open) {
        char *child = malloc(cur_len + 2);
        memcpy(child, cur, cur_len);
        child[cur_len] = ')';
        child[cur_len + 1] = '\0';
        backtrack(child, cur_len + 1, open, close + 1, n, out);
    }
    free(cur); // not retained by the base case on this path
}

static StrVec generate_parenthesis(long n) {
    StrVec out = {0};
    char *root = malloc(1);
    root[0] = '\0';
    backtrack(root, 0, 0, 0, n, &out);
    return out;
}

int main(void) {
    const long n = 10;
    const int iters = 150;
    uint64_t total = 0;
    for (int k = 0; k < iters; k++) {
        StrVec combos = generate_parenthesis(n);
        uint64_t bytes = 0;
        for (size_t j = 0; j < combos.len; j++) {
            bytes += strlen(combos.data[j]);
            free(combos.data[j]);
        }
        free(combos.data);
        total += bytes;
    }
    printf("%llu\n", (unsigned long long)total); // 50,388,000
    return 0;
}
