// LeetCode #2067: Number of Equal Count Substrings -- C mirror of the
// ★ arm's benchmark (count.kara): 60 texts of 30000 letters from 1 to 26
// kinds, half in runs of `count`, count 1 to 7.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t equal_count_substrings(const unsigned char *s, int64_t n, int64_t count) {
    int64_t total = 0;
    for (int64_t k = 1; k <= 26; k++) {
        int64_t len = k * count;
        if (len > n) break;
        int64_t seen[26] = {0};
        int64_t exact = 0;
        for (int64_t i = 0; i < n; i++) {
            int c = s[i] - 'a';
            seen[c]++;
            if (seen[c] == count)
                exact++;
            else if (seen[c] == count + 1)
                exact--;
            if (i >= len) {
                int d = s[i - len] - 'a';
                if (seen[d] == count) exact--;
                seen[d]--;
                if (seen[d] == count) exact++;
            }
            if (i + 1 >= len && exact == k) total++;
        }
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t text_of(unsigned char *out, int64_t n, int64_t k, int64_t count, int64_t p, int64_t *seed) {
    int64_t len = 0;
    while (len < n) {
        unsigned char c = 'a' + next_random(seed) % k;
        int64_t run = next_random(seed) % 100 < p ? count : 1;
        if (run > n - len) run = n - len;
        for (int64_t j = 0; j < run; j++) out[len + j] = c;
        len += run;
    }
    return len;
}

int main(void) {
    int64_t seed = 2067, total = 0, check = 0;
    unsigned char *s = malloc(30000);
    for (int64_t t = 0; t < 60; t++) {
        int64_t count = t % 7 + 1;
        int64_t n = text_of(s, 30000, t % 26 + 1, count, 50, &seed);
        int64_t a = equal_count_substrings(s, n, count);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("60 texts: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(s);
    return 0;
}
