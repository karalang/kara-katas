// LeetCode #680: Valid Palindrome II -- two pointers. Bench.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 300
#define LEN 20000
#define ROUNDS 100

static int64_t seed = 680;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static bool is_palindrome(const char *b, int64_t i, int64_t j) {
    while (i < j) {
        if (b[i] != b[j]) return false;
        i++;
        j--;
    }
    return true;
}

static bool valid_palindrome(const char *b, int64_t n) {
    int64_t i = 0, j = n - 1;
    while (i < j) {
        if (b[i] != b[j])
            return is_palindrome(b, i + 1, j) || is_palindrome(b, i, j - 1);
        i++;
        j--;
    }
    return true;
}

int main(void) {
    static const int64_t widths[3] = {2, 3, 26};
    char *strings[COUNT];
    int64_t lens[COUNT];
    for (int64_t k = 0; k < COUNT; k++) {
        int64_t width = widths[k % 3];
        int64_t extra = k / 3 % 3;
        char *s = malloc(LEN + extra + 1);
        int64_t n = 0;
        for (int64_t i = 0; i < LEN / 2; i++) s[n++] = 'a' + next_random() % width;
        for (int64_t i = LEN / 2 - 1; i >= 0; i--) s[n++] = s[i];
        for (int64_t e = 0; e < extra; e++) {
            int64_t at = next_random() % (n + 1);
            memmove(s + at + 1, s + at, n - at);
            s[at] = 'a' + next_random() % width;
            n++;
        }
        strings[k] = s;
        lens[k] = n;
    }
    int64_t valid = 0, sum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t k = 0; k < COUNT; k++) {
            int64_t at = (k * 7 + r) % COUNT;
            if (valid_palindrome(strings[at], lens[at])) {
                valid++;
                sum = (sum * 31 + at + 1) % 1000000007;
            } else {
                sum = (sum * 31 + 7) % 1000000007;
            }
        }
    }
    printf("%d strings checked: %lld valid, checksum %lld\n", COUNT * ROUNDS,
           (long long)valid, (long long)sum);
    return 0;
}
