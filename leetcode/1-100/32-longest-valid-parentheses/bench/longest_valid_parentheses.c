/* LeetCode #32 bench — C (mirror of longest_valid_parentheses.kara).
 *
 * The index-stack longest-valid-parens. C is the no-GC floor; the per-call
 * stack is a malloc/free pair (the realistic stack-approach allocation), the
 * sliding window over a fixed pseudo-random parens buffer is folded to a sum.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t longest_valid_window(const unsigned char *buf, int64_t start, int64_t w) {
    int64_t *stack = malloc(sizeof(int64_t) * (size_t)(w + 1));
    int64_t sp = 0;
    stack[sp++] = -1;
    int64_t best = 0;
    for (int64_t i = 0; i < w; i++) {
        if (buf[start + i] == '(') {
            stack[sp++] = i;
        } else {
            sp--; /* pop */
            if (sp == 0) {
                stack[sp++] = i;
            } else {
                int64_t top = stack[sp - 1];
                int64_t len = i - top;
                if (len > best) {
                    best = len;
                }
            }
        }
    }
    free(stack);
    return best;
}

int main(void) {
    const int64_t big_l = 4096;
    const int64_t w = 2048;
    const int64_t total = 330000;
    const int64_t modulus = 1000000007;

    unsigned char *buf = malloc((size_t)big_l);
    int64_t x = 0x12345;
    for (int64_t p = 0; p < big_l; p++) {
        x = (x * 1103515245 + 12345) & 0x7fffffff;
        buf[p] = ((x & 1) == 0) ? '(' : ')';
    }

    int64_t span = big_l - w + 1;
    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t start = (k * 7) % span;
        int64_t r = longest_valid_window(buf, start, w);
        acc = (acc + r) % modulus;
    }

    free(buf);
    printf("%lld\n", (long long)acc);
    return 0;
}
