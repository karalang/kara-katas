// Benchmark for #402: mirror of remove_k_digits.kara (a stack that keeps
// digits rising). Each number and each result is a heap buffer, freed
// after its call, as the other mirrors' strings are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *remove_kdigits(const char *num, int64_t n, int64_t k, int64_t *out_len) {
    int64_t left = k;
    char *stack = malloc(n + 1);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) {
        char c = num[i];
        while (left > 0 && top > 0 && stack[top - 1] > c) {
            top--;
            left--;
        }
        stack[top++] = c;
    }
    while (left > 0) {
        top--;
        left--;
    }
    char *out = malloc(top + 2);
    int64_t len = 0;
    for (int64_t i = 0; i < top; i++) {
        if (len == 0 && stack[i] == '0') {
            continue;
        }
        out[len++] = stack[i];
    }
    if (len == 0) {
        out[len++] = '0';
    }
    out[len] = 0;
    free(stack);
    *out_len = len;
    return out;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t numbers = argc > 1 ? atoll(argv[1]) : 300;
    int64_t n = 100000;
    int64_t seed = 402, kept = 0, checksum = 0;
    for (int64_t t = 0; t < numbers; t++) {
        char *num = malloc(n + 1);
        num[0] = (char)(49 + step(&seed) % 9);
        for (int64_t i = 1; i < n; i++) {
            num[i] = (char)(48 + step(&seed) % 10);
        }
        num[n] = 0;
        int64_t k = step(&seed) % (n + 1);
        int64_t len;
        char *r = remove_kdigits(num, n, k, &len);
        kept += len;
        for (int64_t i = 0; i < len; i++) {
            checksum = (checksum * 31 + (unsigned char)r[i]) % 1000000007;
        }
        free(r);
        free(num);
    }
    printf("%lld numbers of %lld digits: %lld digits kept, checksum %lld\n", (long long)numbers, (long long)n, (long long)kept, (long long)checksum);
    return 0;
}
