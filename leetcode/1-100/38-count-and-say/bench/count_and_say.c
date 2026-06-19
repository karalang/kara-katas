// LeetCode #38 bench — C (mirror of count_and_say.kara).
//
// Streaming run-length "say" over a growing digit string held in a malloc'd buffer.
// Workload: TOTAL times seed with the decimal digits of k+1, apply STEPS say-steps, fold
// a position-weighted digit signature of the final term into a checksum. `clang -O3`.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// A tiny growable byte string (length-tracked, NUL not required).
typedef struct {
    char *buf;
    int64_t len;
    int64_t cap;
} Str;

static void str_init(Str *s) {
    s->cap = 16;
    s->len = 0;
    s->buf = (char *)malloc((size_t)s->cap);
}

static void str_push(Str *s, char c) {
    if (s->len == s->cap) {
        s->cap *= 2;
        s->buf = (char *)realloc(s->buf, (size_t)s->cap);
    }
    s->buf[s->len++] = c;
}

static void str_push_decimal(Str *s, int64_t n) {
    char tmp[20];
    int t = 0;
    if (n == 0) {
        str_push(s, '0');
        return;
    }
    while (n > 0) {
        tmp[t++] = (char)('0' + (n % 10));
        n /= 10;
    }
    while (t > 0) {
        str_push(s, tmp[--t]);
    }
}

// One count-and-say step: RLE of `in` into a fresh Str. Run lengths stay <= 9 in
// this workload (verified max 5), so the count is a single decimal digit appended
// in place — fair, allocation-free across the language mirrors.
static Str say(const Str *in) {
    Str out;
    str_init(&out);
    char run_digit = '0';
    int64_t run_len = 0;
    for (int64_t i = 0; i < in->len; i++) {
        char c = in->buf[i];
        if (run_len != 0 && c == run_digit) {
            run_len++;
        } else {
            if (run_len != 0) {
                str_push(&out, (char)('0' + run_len));
                str_push(&out, run_digit);
            }
            run_digit = c;
            run_len = 1;
        }
    }
    if (run_len != 0) {
        str_push(&out, (char)('0' + run_len));
        str_push(&out, run_digit);
    }
    return out;
}

int main(void) {
    const int64_t total = 12000;
    const int64_t steps = 14;
    const int64_t modulus = 1000000007;

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        Str cur;
        str_init(&cur);
        str_push_decimal(&cur, k + 1);
        for (int64_t step = 0; step < steps; step++) {
            Str next = say(&cur);
            free(cur.buf);
            cur = next;
        }

        int64_t sig = 0;
        for (int64_t i = 0; i < cur.len; i++) {
            int64_t dv = (int64_t)(cur.buf[i] - '0');
            sig += dv * (i + 1);
        }
        free(cur.buf);
        acc = (acc * 31 + sig) % modulus;
    }

    printf("%lld\n", (long long)acc);
    return 0;
}
