// LeetCode #2262: Total Appeal of A String -- C mirror of the ★ arm
// (appeal.kara): each position counts the substrings where its letter
// first appears, (i - last) * (n - i), with the last position kept per
// letter. Output is byte-identical to appeal.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t appeal_sum(const char *s, int64_t n) {
    int64_t last[26];
    for (int c = 0; c < 26; c++) last[c] = -1;
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        int c = s[i] - 'a';
        total += (i - last[c]) * (n - i);
        last[c] = i;
    }
    return total;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2262;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    char *s = malloc(100000);
    for (int t = 0; t < 40; t++) {
        int64_t letters = t % 26 + 1;
        for (int i = 0; i < 100000; i++) s[i] = (char)('a' + next_random() % letters);
        check = (check * 31 + appeal_sum(s, 100000)) % 1000000007;
    }
    free(s);
    printf("40 strings of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
