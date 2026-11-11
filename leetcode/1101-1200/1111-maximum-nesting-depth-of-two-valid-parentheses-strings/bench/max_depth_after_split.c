// LeetCode #1111: Maximum Nesting Depth of Two Valid Parentheses Strings
// -- the bench in C: the ★ arm over the same 16 strings and the same
// valid prefixes, each answer a fresh malloc'd array as Kāra's Vec is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t *max_depth_after_split(const char *seq, size_t n) {
    int32_t depth = 0;
    int32_t *answer = malloc(n * sizeof(int32_t));
    for (size_t i = 0; i < n; i++) {
        if (seq[i] == '(') {
            answer[i] = depth % 2;
            depth++;
        } else {
            depth--;
            answer[i] = depth % 2;
        }
    }
    return answer;
}

static int64_t seed = 1111;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    char *s;
    size_t *cuts;
    size_t ncuts;
} Entry;

static Entry random_vps(int64_t pairs) {
    Entry e;
    e.s = malloc(2 * pairs);
    e.cuts = malloc(pairs * sizeof(size_t));
    e.ncuts = 0;
    size_t len = 0;
    int64_t opens = 0, depth = 0;
    while (opens < pairs || depth > 0) {
        if (opens < pairs && (depth == 0 || next_random() % 2 == 0)) {
            e.s[len++] = '(';
            opens++;
            depth++;
        } else {
            e.s[len++] = ')';
            depth--;
            if (depth == 0) e.cuts[e.ncuts++] = len;
        }
    }
    return e;
}

int main(void) {
    Entry strings[16];
    for (int i = 0; i < 16; i++) strings[i] = random_vps(5000);
    int64_t chars = 0, ones = 0, check = 0;
    for (int64_t round = 0; round < 1000; round++) {
        for (int64_t j = 0; j < 16; j++) {
            Entry *e = &strings[j];
            size_t cut = e->cuts[(round * 7919 + j * 104729) % e->ncuts];
            int32_t *answer = max_depth_after_split(e->s, cut);
            chars += cut;
            for (size_t i = 0; i < cut; i++) ones += answer[i];
            check = (check * 31 + answer[(round * 31 + j) % cut]) % 1000000007;
            free(answer);
        }
    }
    printf("1000 rounds over 16 strings of 10000 characters: %lld characters, %lld in the second group, checksum %lld\n",
           (long long)chars, (long long)ones, (long long)check);
    return 0;
}
