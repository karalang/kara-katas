// LeetCode #2396: Strictly Palindromic Number -- the bench, the ★ arm in
// C: every base tried, each base's digits taken into a list and checked
// from both ends.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int palindrome_in_base(int64_t n, int64_t b) {
    int64_t cap = 8, len = 0;
    int64_t *digits = malloc(cap * sizeof *digits);
    for (int64_t m = n; m > 0; m /= b) {
        if (len == cap) {
            cap *= 2;
            digits = realloc(digits, cap * sizeof *digits);
        }
        digits[len++] = m % b;
    }
    int ok = 1;
    for (int64_t i = 0, j = len - 1; i < j; i++, j--) {
        if (digits[i] != digits[j]) {
            ok = 0;
            break;
        }
    }
    free(digits);
    return ok;
}

static int is_strictly_palindromic(int64_t n) {
    for (int64_t b = 2; b < n - 1; b++)
        if (!palindrome_in_base(n, b)) return 0;
    return 1;
}

int main(void) {
    int64_t check = 0, total = 0;
    for (int64_t n = 4; n <= 10000; n++) {
        int64_t count = 0;
        for (int64_t b = 2; b < n - 1; b++) count += palindrome_in_base(n, b);
        total += count;
        check = (check * 31 + count + is_strictly_palindromic(n)) % 1000000007;
    }
    printf("every base of every n from 4 to 10000: checksum %lld, %lld palindromes\n", (long long)check,
           (long long)total);
    return 0;
}
