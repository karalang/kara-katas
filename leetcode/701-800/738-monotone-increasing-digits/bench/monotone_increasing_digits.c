// LeetCode #738: Monotone Increasing Digits -- one drop, then nines.
// Benchmark mirror of the Kara star arm: the digits in a growable
// array, the first place where a digit is larger than the next, a step
// back over equal digits before it, that digit lowered by one and every
// digit after it made a 9.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static int64_t monotone_increasing_digits(int64_t n) {
    Vec digits = {0, 0, 0};
    int64_t x = n;
    while (x > 0) {
        push(&digits, x % 10);
        x /= 10;
    }
    for (int64_t a = 0, b = digits.len - 1; a < b; a++, b--) {
        int64_t t = digits.data[a];
        digits.data[a] = digits.data[b];
        digits.data[b] = t;
    }
    int64_t i = 0;
    while (i + 1 < digits.len && digits.data[i] <= digits.data[i + 1]) i++;
    if (i + 1 < digits.len) {
        while (i > 0 && digits.data[i - 1] == digits.data[i]) i--;
        digits.data[i] -= 1;
        for (int64_t j = i + 1; j < digits.len; j++) digits.data[j] = 9;
    }
    int64_t out = 0;
    for (int64_t j = 0; j < digits.len; j++) out = out * 10 + digits.data[j];
    free(digits.data);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 738, total = 0, kept = 0;
    for (int k = 0; k < 3000000; k++) {
        int64_t a = next_random(&seed);
        int64_t b = next_random(&seed);
        int64_t n = (a * 32768 + b) % 1000000001;
        int64_t m = monotone_increasing_digits(n);
        if (m == n) kept++;
        total += m;
    }
    printf("3000000 random numbers: %lld already monotone, answers sum to %lld\n", (long long)kept, (long long)total);
    return 0;
}
