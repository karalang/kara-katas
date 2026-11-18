// LeetCode #1616: Split Two Strings to Make Palindrome -- the bench in C,
// mirroring split.kara: two pointers, a from the front against b from the
// back as far as they agree, then whether the middle left over, of a or
// of b, is a palindrome by itself; then the roles swapped.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PAIRS 10
#define N 500000
#define CHECKS 30

static bool is_palindrome(const char *s, int64_t lo, int64_t hi) {
    int64_t i = lo, j = hi;
    while (i < j) {
        if (s[i] != s[j]) return false;
        i++;
        j--;
    }
    return true;
}

static bool joins(const char *a, const char *b, int64_t n) {
    int64_t i = 0, j = n - 1;
    while (i < j && a[i] == b[j]) {
        i++;
        j--;
    }
    return is_palindrome(a, i, j) || is_palindrome(b, i, j);
}

static bool check_palindrome_formation(const char *a, const char *b, int64_t n) {
    return joins(a, b, n) || joins(b, a, n);
}

static int64_t seed = 1616;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static void pair(int64_t n, char *a, char *b) {
    for (int64_t i = 0; i < n; i++) {
        a[i] = (char)('a' + next_random() % 2);
        b[i] = (char)('a' + next_random() % 2);
    }
    int64_t k = next_random() % (n / 2 + 1);
    for (int64_t j = 0; j < k; j++) b[n - 1 - j] = a[j];
    for (int64_t j = 0; j < (n - 2 * k) / 2; j++) b[n - k - 1 - j] = b[k + j];
    if (next_random() % 2 == 0) {
        int64_t i = next_random() % n;
        b[i] = (char)('a' + next_random() % 2);
    }
}

int main(void) {
    char *as[PAIRS], *bs[PAIRS];
    for (int p = 0; p < PAIRS; p++) {
        as[p] = malloc(N);
        bs[p] = malloc(N);
        pair(N, as[p], bs[p]);
    }
    int64_t check = 0, yes = 0;
    for (int p = 0; p < PAIRS; p++)
        for (int c = 0; c < CHECKS; c++) {
            bool answer = check_palindrome_formation(as[p], bs[p], N);
            if (answer) yes++;
            check = mix(check, answer ? 1 : 0);
        }
    printf("%d pairs of %d letters from 2, each checked %d times: %lld split, checksum %lld\n", PAIRS, N, CHECKS,
           (long long)yes, (long long)check);
    for (int p = 0; p < PAIRS; p++) {
        free(as[p]);
        free(bs[p]);
    }
    return 0;
}
