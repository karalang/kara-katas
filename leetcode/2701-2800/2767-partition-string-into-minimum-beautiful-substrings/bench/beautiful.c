// LeetCode #2767: Partition String Into Minimum Beautiful Substrings --
// the bench in C: the ★ arm over 100000 strings of 15 binary digits, all
// drawn first, then each answered 5 times. Each piece's value is read
// digit by digit, as from_str_radix reads it.

#include <stdio.h>
#include <string.h>

static int is_power_of_five(long long v) {
    while (v > 1 && v % 5 == 0) {
        v /= 5;
    }
    return v == 1;
}

static long long minimum_beautiful_substrings(const char *s, int n) {
    long long best[32];
    for (int i = 0; i <= n; i++) {
        best[i] = -1;
    }
    best[0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            if (best[j] < 0 || s[j] != '1') {
                continue;
            }
            long long value = 0;
            for (int k = j; k < i; k++) {
                value = value * 2 + (s[k] - '0');
            }
            if (is_power_of_five(value) && (best[i] < 0 || best[j] + 1 < best[i])) {
                best[i] = best[j] + 1;
            }
        }
    }
    return best[n];
}

static long long seed = 2767;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define COUNT 100000

static char strings[COUNT][16];

int main(void) {
    int rounds = 5;
    const char *powers[] = {"1", "101", "11001", "1111101", "1001110001", "110000110101", "11110100001001"};
    for (int c = 0; c < COUNT; c++) {
        char *s = strings[c];
        int len = 0;
        s[0] = 0;
        for (;;) {
            const char *p = powers[next_random() % 7];
            int pl = (int)strlen(p);
            if (len + pl > 15) {
                break;
            }
            memcpy(s + len, p, pl);
            len += pl;
        }
        while (len < 15) {
            s[len++] = next_random() % 2 == 1 ? '1' : '0';
        }
        s[len] = 0;
        if (next_random() % 2 == 1) {
            int k = (int)(next_random() % 15);
            s[k] = s[k] == '1' ? '0' : '1';
        }
    }
    long long split = 0, pieces = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            long long a = minimum_beautiful_substrings(strings[c], 15);
            if (a > 0) {
                split += 1;
                pieces += a;
            }
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    printf("%d strings of 15, %d rounds: %lld split, pieces sum to %lld, checksum %lld\n", COUNT, rounds, split, pieces, check);
    return 0;
}
