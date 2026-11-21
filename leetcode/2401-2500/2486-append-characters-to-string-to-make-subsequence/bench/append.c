// LeetCode #2486: Append Characters to String to Make Subsequence --
// bench, C mirror of append.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t append_characters(const char *s, const char *t) {
    int64_t m = (int64_t)strlen(t), matched = 0;
    for (const char *c = s; *c; c++)
        if (matched < m && *c == t[matched]) matched += 1;
    return m - matched;
}

static int64_t seed = 2486;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char letters[4] = {'a', 'b', 'c', 'd'};
    static char s[20][10000], t[20][10001];
    for (int g = 0; g < 20; g++) {
        for (int i = 0; i < 10000; i++) s[g][i] = letters[next_random() % 4];
        for (int i = 0; i < 10000; i++) t[g][i] = letters[next_random() % 4];
        t[g][10000] = 0;
    }
    static char joined[10001];
    int64_t check = 0;
    for (int64_t p = 0; p < 600; p++) {
        for (int g = 0; g < 20; g++) {
            s[g][check % 10000] = letters[check / 10000 % 4];
            memcpy(joined, s[g], 10000);
            joined[10000] = 0;
            check = (check * 31 + append_characters(joined, t[g]) + p) % 1000000007;
        }
    }
    printf("600 passes over 20 pairs of 10^4 letters: checksum %lld\n", (long long)check);
    return 0;
}
