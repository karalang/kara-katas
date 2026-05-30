// Benchmark workload — Letter Combinations of a Phone Number (LeetCode #17).
// C mirror of bench/letter_combinations.kara. Same M/K, generator, BFS shape,
// and sink — see that file's header for the workload rationale.
//
// Each combo is a malloc'd char buffer; the per-call output is a malloc'd
// array of char-buffer pointers. Both are freed before the next iter, so
// the per-iter alloc/free shape mirrors the .kara version's Vec[String]
// fresh-alloc + scope-drop pattern (a fair comparator for the allocator
// noise floor, BENCH.md § Mirror per-iter allocation parity).

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    char **items;
    int    count;
} Combos;

static void combos_free(Combos *c) {
    for (int i = 0; i < c->count; i++) free(c->items[i]);
    free(c->items);
}

static Combos letter_combinations(const char *digits) {
    static const char *groups[8] = {
        "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };
    Combos out = {NULL, 0};
    size_t dlen = strlen(digits);
    if (dlen == 0) return out;

    // Seed frontier with the empty string.
    out.items = (char **)malloc(sizeof(char *));
    out.items[0] = (char *)calloc(1, 1);
    out.count = 1;

    for (size_t d = 0; d < dlen; d++) {
        int idx = digits[d] - '2';
        const char *letters = groups[idx];
        int letters_len = (int)strlen(letters);
        int prev_len = out.count;
        int next_cap = prev_len * letters_len;
        Combos next;
        next.items = (char **)malloc(sizeof(char *) * (size_t)next_cap);
        next.count = next_cap;
        int w = 0;
        for (int i = 0; i < prev_len; i++) {
            int plen = (int)strlen(out.items[i]);
            for (int j = 0; j < letters_len; j++) {
                char *s = (char *)malloc((size_t)plen + 2);
                memcpy(s, out.items[i], (size_t)plen);
                s[plen] = letters[j];
                s[plen + 1] = '\0';
                next.items[w++] = s;
            }
        }
        combos_free(&out);
        out = next;
    }
    return out;
}

int main(void) {
    const int64_t m_cases = 8;
    const int64_t k_iters = 100000;
    static const char *cases[8] = {"", "2", "7", "23", "79", "234", "279", "2349"};

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % m_cases;
        Combos r = letter_combinations(cases[idx]);
        sum += (int64_t)r.count;
        combos_free(&r);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
