// Benchmark for #537: C mirror of the ★ arm (split, then the schoolbook
// product); see complex_number_multiply.kara. The number is split at
// its '+' into two pieces, each read with strtoll, and the product is
// written into a fresh malloc'd string, as the ★ arm returns a fresh
// `String`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void parts(const char *num, int64_t *re, int64_t *im) {
    const char *plus = strchr(num, '+');
    *re = strtoll(num, NULL, 10);
    *im = strtoll(plus + 1, NULL, 10);
}

static char *complex_number_multiply(const char *num1, const char *num2) {
    int64_t a, b, c, d;
    parts(num1, &a, &b);
    parts(num2, &c, &d);
    char buf[48];
    int n = snprintf(buf, sizeof buf, "%lld+%lldi", (long long)(a * c - b * d), (long long)(a * d + b * c));
    char *out = malloc(n + 1);
    memcpy(out, buf, n + 1);
    return out;
}

static int64_t seed = 537;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { N = 2000 };
    static char nums[N][16];
    for (int i = 0; i < N; i++) {
        int64_t re = next_random() % 201 - 100;
        int64_t im = next_random() % 201 - 100;
        snprintf(nums[i], sizeof nums[i], "%lld+%lldi", (long long)re, (long long)im);
    }
    int64_t rounds = 2500;
    int64_t real = 0, length = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < N; i++) {
            char *p = complex_number_multiply(nums[i], nums[(i * 7 + r) % N]);
            size_t len = strlen(p);
            if (len >= 3 && strcmp(p + len - 3, "+0i") == 0) real++;
            length += (int64_t)len;
            free(p);
        }
    }
    printf("%d numbers, %lld rounds: %lld real, length %lld\n", N, (long long)rounds, (long long)real, (long long)length);
    return 0;
}
