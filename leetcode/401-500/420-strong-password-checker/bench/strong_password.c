// LeetCode #420: Strong Password Checker -- C mirror of
// strong_password.kara (count the runs by length mod 3).
// Usage: ./strong_password [calls]
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }
static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t strong_password_checker(const char *p, int64_t n) {
    int64_t lower = 0, upper = 0, digit = 0;
    for (int64_t k = 0; k < n; k++) {
        char b = p[k];
        if (b >= 'a' && b <= 'z') {
            lower = 1;
        } else if (b >= 'A' && b <= 'Z') {
            upper = 1;
        } else if (b >= '0' && b <= '9') {
            digit = 1;
        }
    }
    int64_t missing = 3 - lower - upper - digit;
    int64_t replace = 0, zero_mod = 0, one_mod = 0;
    int64_t i = 0;
    while (i < n) {
        int64_t j = i;
        while (j < n && p[j] == p[i]) {
            j += 1;
        }
        int64_t run = j - i;
        if (run >= 3) {
            replace += run / 3;
            if (run % 3 == 0) {
                zero_mod += 1;
            } else if (run % 3 == 1) {
                one_mod += 1;
            }
        }
        i = j;
    }
    if (n < 6) {
        return max64(missing, 6 - n);
    }
    if (n <= 20) {
        return max64(missing, replace);
    }
    int64_t del = n - 20, left = del;
    int64_t first = min64(left, zero_mod);
    replace -= first;
    left -= first;
    int64_t second = min64(left, 2 * one_mod);
    replace -= second / 2;
    left -= second;
    replace -= min64(left / 3, replace);
    return del + max64(missing, replace);
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 10000000;
    int64_t seed = 420;
    const char *pool = "aAbB1.";
    char *text = malloc(1000000 + 8);
    int64_t len = 0;
    while (len < 1000000) {
        char pick = pool[step(&seed) % 6];
        int64_t run = 1 + step(&seed) % 6;
        for (int64_t k = 0; k < run; k++) {
            text[len++] = pick;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t c = 0; c < calls; c++) {
        int64_t length = 1 + step(&seed) % 50;
        int64_t start = step(&seed) * 30 % (1000000 - length);
        int64_t answer = strong_password_checker(text + start, length);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)checksum);
    free(text);
    return 0;
}
