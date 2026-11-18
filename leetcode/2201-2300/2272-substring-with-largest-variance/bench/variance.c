// LeetCode #2272: Substring With Largest Variance -- the bench, the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t largest_variance(const char *s, int64_t n) {
    int seen[26] = {0};
    for (int64_t i = 0; i < n; i++) seen[s[i] - 'a'] = 1;
    int64_t best = 0;
    for (char a = 'a'; a <= 'z'; a++) {
        for (char b = 'a'; b <= 'z'; b++) {
            if (a == b || !seen[a - 'a'] || !seen[b - 'a']) continue;
            int64_t diff = 0, with_b = INT64_MIN / 2;
            for (int64_t i = 0; i < n; i++) {
                char c = s[i];
                if (c == a) {
                    diff++;
                    with_b++;
                } else if (c == b) {
                    with_b = diff - 1;
                    diff = diff - 1 > 0 ? diff - 1 : 0;
                }
                if (with_b > best) best = with_b;
            }
        }
    }
    return best;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2272;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t ks[] = {3, 5, 10, 26};
    char *s = malloc(10000);
    int64_t check = 0;
    for (int t = 0; t < 40; t++) {
        int64_t k = ks[t % 4];
        for (int i = 0; i < 10000; i++) s[i] = (char)('a' + next_random() % k);
        check = (check * 31 + largest_variance(s, 10000)) % 1000000007;
    }
    free(s);
    printf("40 strings of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
