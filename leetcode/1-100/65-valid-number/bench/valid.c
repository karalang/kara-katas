// Benchmark workload — 8-state DFA over `s.bytes()` for LeetCode #65.
// C mirror of bench/valid.kara. Same N, K, input set, sink formula —
// see that file's header for the workload rationale.
//
// Built via `clang -O3` in bench.sh. C is in the harness as the
// upper bound of "what a hand-rolled scalar baseline looks like" —
// same algorithm rust runs serially with one less abstraction layer
// (no `&str` length-prefixed slice, just `strlen` + raw `char*`).

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

static int32_t categorize(unsigned char b) {
    if (b >= '0' && b <= '9') return 0;
    if (b == '+' || b == '-') return 1;
    if (b == '.')             return 2;
    if (b == 'e' || b == 'E') return 3;
    return 4;
}

static int is_number(const char *s) {
    size_t n = strlen(s);

    int32_t state = 0;
    for (size_t i = 0; i < n; i++) {
        int32_t cat = categorize((unsigned char)s[i]);

        if (state == 0) {
            switch (cat) {
                case 0: state = 2; break;
                case 1: state = 1; break;
                case 2: state = 3; break;
                default: return 0;
            }
        } else if (state == 1) {
            switch (cat) {
                case 0: state = 2; break;
                case 2: state = 3; break;
                default: return 0;
            }
        } else if (state == 2) {
            switch (cat) {
                case 0: state = 2; break;
                case 2: state = 4; break;
                case 3: state = 6; break;
                default: return 0;
            }
        } else if (state == 3) {
            switch (cat) {
                case 0: state = 5; break;
                default: return 0;
            }
        } else if (state == 4) {
            switch (cat) {
                case 0: state = 5; break;
                case 3: state = 6; break;
                default: return 0;
            }
        } else if (state == 5) {
            switch (cat) {
                case 0: state = 5; break;
                case 3: state = 6; break;
                default: return 0;
            }
        } else if (state == 6) {
            switch (cat) {
                case 0: state = 8; break;
                case 1: state = 7; break;
                default: return 0;
            }
        } else if (state == 7) {
            switch (cat) {
                case 0: state = 8; break;
                default: return 0;
            }
        } else if (state == 8) {
            switch (cat) {
                case 0: state = 8; break;
                default: return 0;
            }
        } else {
            return 0;
        }
    }

    return state == 2 || state == 4 || state == 5 || state == 8;
}

int main(void) {
    const int64_t n = 8;
    const int64_t k_iters = 10000000;

    const char *inputs[8] = {
        "0",
        "-.9",
        "53.5e93",
        "+6e-1",
        "abc",
        "1e",
        "99e2.5",
        "-123.456e789",
    };

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % n;
        if (is_number(inputs[idx])) {
            sum += 1;
        }
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
