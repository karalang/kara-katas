// Benchmark workload — one-pass atoi (LeetCode #8). C mirror of
// bench/atoi.kara. Same N, K, same input set, same sink formula —
// see that file's header for the workload rationale.
//
// Built via `clang -O3` in bench.sh. C is in the harness as the
// upper bound of "what a hand-rolled scalar baseline looks like" —
// it's the same algorithm rust runs serially, with one less abstraction
// layer (no `&str` length-prefixed slice, just `strlen` + raw `char*`).

#include <stdio.h>
#include <stdint.h>
#include <string.h>

static int32_t my_atoi(const char *s) {
    size_t n = strlen(s);

    size_t i = 0;
    while (i < n && s[i] == ' ') {
        i++;
    }

    int32_t sign = 1;
    if (i < n && s[i] == '+') {
        i++;
    } else if (i < n && s[i] == '-') {
        sign = -1;
        i++;
    }

    const int32_t int_max = 2147483647;
    const int32_t int_min = -2147483648;
    const int32_t max_div = int_max / 10;

    int32_t result = 0;
    while (i < n) {
        unsigned char b = (unsigned char)s[i];
        if (b < '0' || b > '9') {
            break;
        }
        int32_t digit = (int32_t)(b - '0');
        if (result > max_div || (result == max_div && digit > 7)) {
            return sign == 1 ? int_max : int_min;
        }
        result = result * 10 + digit;
        i++;
    }

    return sign * result;
}

int main(void) {
    const int64_t n = 8;
    const int64_t k_iters = 10000000;

    const char *inputs[8] = {
        "42",
        "   -42",
        "4193 with words",
        "91283472332",
        "+1",
        "  0000000000012345678",
        "-2147483648",
        "  -0012a42",
    };

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % n;
        sum += (int64_t)my_atoi(inputs[idx]);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
