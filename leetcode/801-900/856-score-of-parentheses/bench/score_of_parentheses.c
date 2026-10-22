// Benchmark for #856: Score of Parentheses -- the ★ arm, mirroring
// score_of_parentheses.kara. The stack grows on the heap as in the other
// languages.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t score_of_parentheses(const char *s) {
    int64_t cap = 4, len = 1;
    int64_t *stack = malloc(cap * sizeof(int64_t));
    stack[0] = 0;
    for (const char *c = s; *c; c++) {
        if (*c == '(') {
            if (len == cap) {
                cap *= 2;
                stack = realloc(stack, cap * sizeof(int64_t));
            }
            stack[len++] = 0;
        } else {
            int64_t inner = stack[--len];
            int64_t worth = inner == 0 ? 1 : 2 * inner;
            stack[len - 1] += worth;
        }
    }
    int64_t out = stack[0];
    free(stack);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 64, rounds = 4000000, seed = 856;
    char strings[64][51];
    for (int64_t g = 0; g < count; g++) {
        int64_t len = 0, opens = 0, balance = 0;
        while (len < 50) {
            if (opens < 25 && (balance == 0 || next_random(&seed) % 4 < 1 + g % 3)) {
                strings[g][len++] = '(';
                opens++;
                balance++;
            } else {
                strings[g][len++] = ')';
                balance--;
            }
        }
        strings[g][len] = 0;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t k = score_of_parentheses(strings[round % count]);
        total += k;
        checksum = (checksum * 31 + k) % 1000000007;
    }
    printf("%lld rounds of 64 strings: scores sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)total, (long long)checksum);
    return 0;
}
