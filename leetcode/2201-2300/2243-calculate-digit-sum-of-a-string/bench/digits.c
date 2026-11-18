// LeetCode #2243: Calculate Digit Sum of a String -- the benchmark's C
// mirror of digits.kara: while the string is longer than k, it is
// rebuilt group by group, each group's digits summed and the sum written
// back. Each round writes into a second buffer of the same size.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

// writes the answer into `out` (at least 101 bytes) and returns its length
static size_t digit_sum(const char *s, size_t k, char *out) {
    char a[128], b[128];
    size_t len = strlen(s);
    memcpy(a, s, len + 1);
    char *current = a, *next = b;
    while (len > k) {
        size_t n = 0;
        for (size_t start = 0; start < len; start += k) {
            size_t end = start + k < len ? start + k : len;
            int64_t sum = 0;
            for (size_t i = start; i < end; i++) sum += current[i] - '0';
            n += (size_t)snprintf(next + n, sizeof a - n, "%lld", (long long)sum);
        }
        char *t = current;
        current = next;
        next = t;
        len = n;
    }
    memcpy(out, current, len + 1);
    return len;
}

static int64_t seed = 2243;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void digits_of(char *s) {
    for (int i = 0; i < 100; i++) s[i] = (char)('0' + next_random() % 10);
    s[100] = 0;
}

int main(void) {
    static char strings[1000][101];
    char answer[128];
    for (int i = 0; i < 1000; i++) digits_of(strings[i]);
    int64_t check = 0;
    for (int pass = 0; pass < 200; pass++) {
        int64_t at = next_random() % 1000;
        digits_of(strings[at]);
        size_t k = (size_t)(pass % 4 + 2);
        for (int i = 0; i < 1000; i++) {
            size_t n = digit_sum(strings[i], k, answer);
            for (size_t j = 0; j < n; j++) check = (check * 31 + answer[j]) % 1000000007;
        }
    }
    printf("200 passes over 1000 strings: checksum %lld\n", (long long)check);
    return 0;
}
