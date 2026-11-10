// LeetCode #2081: Sum of k-Mirror Numbers -- C mirror of the ★ arm's
// benchmark (kmirror.kara): every base from 2 to 9 asked for every `n`
// from 1 to 32, each search started afresh: 256 searches. The base-`k`
// digits go into a growable array, malloc'd per number as Kāra's `Vec`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int is_mirror(int64_t x, int64_t k) {
    int64_t cap = 4, m = 0;
    int64_t *digits = malloc(cap * sizeof(int64_t));
    for (int64_t y = x; y > 0; y /= k) {
        if (m == cap) {
            cap *= 2;
            digits = realloc(digits, cap * sizeof(int64_t));
        }
        digits[m++] = y % k;
    }
    int ok = 1;
    for (int64_t i = 0; i < m / 2; i++) {
        if (digits[i] != digits[m - 1 - i]) {
            ok = 0;
            break;
        }
    }
    free(digits);
    return ok;
}

static int64_t k_mirror(int64_t k, int64_t n) {
    int64_t sum = 0, found = 0;
    for (int64_t length = 1;; length++) {
        int64_t half = (length + 1) / 2, start = 1;
        for (int64_t i = 1; i < half; i++) start *= 10;
        for (int64_t h = start; h < start * 10; h++) {
            int64_t p = h, rest = length % 2 == 1 ? h / 10 : h;
            while (rest > 0) {
                p = p * 10 + rest % 10;
                rest /= 10;
            }
            if (is_mirror(p, k)) {
                sum += p;
                if (++found == n) return sum;
            }
        }
    }
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int64_t k = 2; k < 10; k++) {
        for (int64_t n = 1; n < 33; n++) {
            int64_t a = k_mirror(k, n);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    printf("256 answers: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
