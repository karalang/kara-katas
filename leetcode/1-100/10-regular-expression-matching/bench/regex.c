// Benchmark workload — recursive Regular Expression Matching (LeetCode #10).
// C mirror of bench/regex.kara. Same N, K, same input set, same sink
// formula — see that file's header for the workload rationale.
//
// Built via `clang -O3` in bench.sh. C is in the harness as the
// upper bound of "what a hand-rolled scalar baseline looks like" — same
// algorithm rust and kara run serially, one less abstraction layer (no
// `&str`/`Slice[u8]` length-prefixed slice, just `strlen` + raw `char*`).

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

static bool is_match_at(const char *s, size_t n, size_t i,
                        const char *p, size_t m, size_t j) {
    if (j == m) {
        return i == n;
    }

    bool first_match = i < n && (p[j] == s[i] || p[j] == '.');

    if (j + 1 < m && p[j + 1] == '*') {
        return is_match_at(s, n, i, p, m, j + 2)
            || (first_match && is_match_at(s, n, i + 1, p, m, j));
    }

    return first_match && is_match_at(s, n, i + 1, p, m, j + 1);
}

static bool is_match(const char *s, const char *p) {
    return is_match_at(s, strlen(s), 0, p, strlen(p), 0);
}

int main(void) {
    const int64_t n = 8;
    const int64_t k_iters = 10000000;

    const char *strs[8] = {
        "aa",
        "ab",
        "aab",
        "mississippi",
        "aaaaaaaaaab",
        "aaa",
        "abc",
        "aaab",
    };
    const char *pats[8] = {
        "a*",
        ".*",
        "c*a*b",
        "mis*is*p*.",
        "a*a*a*a*a*b",
        "ab*a",
        "...",
        "a*b",
    };

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % n;
        sum += is_match(strs[idx], pats[idx]) ? 1 : 0;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
