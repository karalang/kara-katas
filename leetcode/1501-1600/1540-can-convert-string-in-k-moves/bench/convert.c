// LeetCode #1540: Can Convert String in K Moves -- bench: the ★ arm (the
// places counted by shift) over 100 pairs of 1 to 20000 letters, each with
// k from 0 to 40000, built once, every pair asked 50 times. C mirror of
// convert.kara.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool can_convert_string(const char *s, int64_t n, const char *t, int64_t m, int64_t k) {
    if (n != m) return false;
    int64_t count[26] = {0};
    for (int64_t i = 0; i < n; i++) {
        int64_t d = ((int64_t)t[i] - (int64_t)s[i] + 26) % 26;
        count[d] += 1;
    }
    for (int64_t d = 1; d < 26; d++) {
        if (count[d] > 0 && d + 26 * (count[d] - 1) > k) return false;
    }
    return true;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static char *word(int64_t n, int64_t letters, int64_t *seed) {
    char *w = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) {
        w[i] = (char)('a' + next_random(seed) % letters);
    }
    w[n] = 0;
    return w;
}

int main(void) {
    int64_t seed = 1540;
    char *ss[100], *ts[100];
    int64_t ns[100], ks[100];
    for (int p = 0; p < 100; p++) {
        int64_t a = next_random(&seed);
        int64_t n = (a * 32768 + next_random(&seed)) % 20000 + 1;
        int64_t used = next_random(&seed) % 26 + 1;
        ss[p] = word(n, used, &seed);
        ts[p] = word(n, used, &seed);
        int64_t b = next_random(&seed);
        ks[p] = (b * 32768 + next_random(&seed)) % 40001;
        ns[p] = n;
    }
    int64_t check = 0, yes = 0;
    for (int r = 0; r < 50; r++) {
        for (int p = 0; p < 100; p++) {
            bool answer = can_convert_string(ss[p], ns[p], ts[p], ns[p], ks[p]);
            if (answer) yes += 1;
            check = mix(check, answer ? 1 : 0);
        }
    }
    for (int p = 0; p < 100; p++) {
        free(ss[p]);
        free(ts[p]);
    }
    printf("50 passes over 100 pairs of up to 20000 letters: %lld true, checksum %lld\n", (long long)yes,
           (long long)check);
    return 0;
}
