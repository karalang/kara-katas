/* Benchmark workload for LeetCode #273 — Integer to English Words.
 *
 * Algorithm-for-algorithm mirror of spell.kara. See that file's header for what
 * this lane measures and for the parity decisions.
 *
 * C has no owned string type, so one is built here explicitly: every string that
 * flows through the algorithm is a malloc'd, NUL-terminated buffer that its
 * holder owns and frees — which is what `String` is in the other four mirrors.
 * `join` allocates a fresh buffer, copies both operands and frees them, exactly
 * as `a + " " + b` does elsewhere. Without that, C would be measuring a
 * hand-rolled arena against four heap allocators. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *own(const char *lit) {
    size_t n = strlen(lit);
    char *p = malloc(n + 1);
    memcpy(p, lit, n + 1);
    return p;
}

/* a + sep + b, consuming both.
 *
 * `realloc` on the LEFT operand rather than a fresh malloc + two copies: that
 * is what an owned-string `+` does in the languages that have one (Rust's
 * `String + &str` consumes and extends the left buffer), and the algorithm's
 * left operand is always the small fresh `piece`. A fresh-malloc version was
 * measured first and cost C about 4% — the difference is one memcpy of a short
 * string — but it would have been C doing more work than the other four, not
 * less, so the realloc form is the honest mirror. */
static char *join(char *a, const char *sep, char *b) {
    size_t la = strlen(a), ls = strlen(sep), lb = strlen(b);
    char *p = realloc(a, la + ls + lb + 1);
    memcpy(p + la, sep, ls);
    memcpy(p + la + ls, b, lb + 1);
    free(b);
    return p;
}

static const char *SMALL[20] = {
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen"};
static const char *TENS[10] = {
    "", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty",
    "Ninety"};
static const char *SCALES[4] = {"", "Thousand", "Million", "Billion"};

static char *group_name(int64_t n) {
    if (n == 0) return own("");
    if (n < 20) return own(SMALL[n]);
    if (n < 100) {
        char *t = own(TENS[n / 10]);
        int64_t r = n % 10;
        if (r == 0) return t;
        return join(t, " ", own(SMALL[r]));
    }
    char *h = join(own(SMALL[n / 100]), " ", own("Hundred"));
    char *r = group_name(n % 100);
    if (r[0] == '\0') { free(r); return h; }
    return join(h, " ", r);
}

static char *number_to_words(int64_t n) {
    if (n == 0) return own("Zero");
    char *out = own("");
    int64_t rem = n, scale = 0;
    while (rem > 0) {
        int64_t part = rem % 1000;
        if (part > 0) {
            char *piece = group_name(part);
            if (scale > 0) piece = join(piece, " ", own(SCALES[scale]));
            if (out[0] == '\0') { free(out); out = piece; }
            else { out = join(piece, " ", out); }
        }
        rem /= 1000;
        scale++;
    }
    return out;
}

int main(void) {
    const int64_t count = 200000;
    const int64_t rounds = 5;

    int64_t *nums = malloc((size_t)count * sizeof(int64_t));
    int64_t lo = 2147483647, hi = 0;
    int64_t state = 273273;
    for (int64_t i = 0; i < count; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        if (state < lo) lo = state;
        if (state > hi) hi = state;
        nums[i] = state;
    }

    int64_t sink = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t q = 0; q < count; q++) {
            char *w = number_to_words(nums[q]);
            for (const unsigned char *p = (const unsigned char *)w; *p; p++) {
                sink = (sink * 131 + (int64_t)*p) % 1000000007;
            }
            free(w);
        }
    }

    printf("%lld\n", (long long)sink);
    printf("count %lld range %lld..%lld\n", (long long)count, (long long)lo, (long long)hi);
    free(nums);
    return 0;
}
