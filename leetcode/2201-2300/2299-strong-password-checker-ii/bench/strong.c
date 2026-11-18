// LeetCode #2299: Strong Password Checker II -- the bench, the ★ arm in
// C. One pass over the letters: a switch sets one of four flags, and the
// letter before must differ from each one.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { COUNT = 200000, MAXLEN = 21 };

static bool strong_password_checker_ii(const char *p, int n) {
    if (n < 8) return false;
    bool lower = false, upper = false, digit = false, special = false;
    char prev = ' ';
    for (int i = 0; i < n; i++) {
        char c = p[i];
        if (c == prev) return false;
        if (c >= 'a' && c <= 'z') lower = true;
        else if (c >= 'A' && c <= 'Z') upper = true;
        else if (c >= '0' && c <= '9') digit = true;
        else switch (c) {
            case '!': case '@': case '#': case '$': case '%': case '^':
            case '&': case '*': case '(': case ')': case '-': case '+':
                special = true;
                break;
            default:
                break;
        }
        prev = c;
    }
    return lower && upper && digit && special;
}

static int64_t seed = 2299;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static const char *kinds[4] = {
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "0123456789",
        "!@#$%^&*()-+",
    };
    static char passwords[COUNT][MAXLEN];
    static int lens[COUNT];
    for (int k = 0; k < COUNT; k++) {
        int64_t n = next_random() % 13 + 8;
        int64_t width = next_random() % 12 + 1;
        for (int64_t j = 0; j < n; j++) {
            const char *kind = kinds[next_random() % 4];
            int64_t len = (int64_t)strlen(kind);
            passwords[k][j] = kind[next_random() % (width < len ? width : len)];
        }
        lens[k] = (int)n;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++)
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t k = (i + 7 * p) % COUNT;
            check = (check * 31 + (strong_password_checker_ii(passwords[k], lens[k]) ? lens[k] : 1)) % 1000000007;
        }
    printf("20 passes over 2 * 10^5 passwords: checksum %lld\n", (long long)check);
    return 0;
}
