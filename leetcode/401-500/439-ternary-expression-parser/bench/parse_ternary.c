// Benchmark for #439: mirror of parse_ternary.kara (a stack, scanning
// from the right) on 200 random expressions of 2,499 ternaries each,
// built once and evaluated 20 times over.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char parse_ternary(const char *e, int64_t n) {
    char *stack = malloc(n);
    int64_t top = 0;
    int64_t i = n;
    while (i > 0) {
        i -= 1;
        if (top > 0 && stack[top - 1] == '?') {
            char yes = stack[top - 2];
            char no = stack[top - 4];
            top -= 4;
            stack[top++] = e[i] == 'T' ? yes : no;
        } else {
            stack[top++] = e[i];
        }
    }
    char value = stack[0];
    free(stack);
    return value;
}

// Appends a random expression of exactly n ternaries at out + *len: a
// random split of the n - 1 below the root between its two branches.
static void random_expression(int64_t *seed, int64_t n, char *out, int64_t *len) {
    if (n == 0) {
        int64_t r = next_random(seed) % 12;
        out[(*len)++] = r < 10 ? (char)('0' + r) : r == 10 ? 'T' : 'F';
        return;
    }
    out[(*len)++] = next_random(seed) % 2 == 0 ? 'T' : 'F';
    out[(*len)++] = '?';
    int64_t left = next_random(seed) % n;
    random_expression(seed, left, out, len);
    out[(*len)++] = ':';
    random_expression(seed, n - 1 - left, out, len);
}

int main(void) {
    const int64_t count = 200, ternaries = 2499, rounds = 20;
    int64_t seed = 439;
    char **expressions = malloc(count * sizeof(char *));
    int64_t *lengths = malloc(count * sizeof(int64_t));
    for (int64_t k = 0; k < count; k++) {
        expressions[k] = malloc(4 * ternaries + 1);
        lengths[k] = 0;
        random_expression(&seed, ternaries, expressions[k], &lengths[k]);
    }
    int64_t digits = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t k = 0; k < count; k++) {
            char value = parse_ternary(expressions[k], lengths[k]);
            if (value != 'T' && value != 'F') {
                digits += 1;
            }
            checksum = (checksum * 31 + value + round) % 1000000007;
        }
    }
    printf("%lld expressions of %lld characters, %lld rounds: %lld digits, checksum %lld\n", (long long)count,
           (long long)lengths[0], (long long)rounds, (long long)digits, (long long)checksum);
    for (int64_t k = 0; k < count; k++) {
        free(expressions[k]);
    }
    free(expressions);
    free(lengths);
    return 0;
}
