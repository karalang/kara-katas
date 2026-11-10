// LeetCode #2083: Substrings That Begin and End With the Same Letter -- C
// mirror of the ★ arm's benchmark (same.kara): one text of 10^6 letters
// built once, then 5000 windows of 10^5 letters counted through a pointer
// and a length into the text.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2083;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t number_of_substrings(const char *s, int64_t n) {
    int64_t counts[26] = {0};
    for (int64_t i = 0; i < n; i++) counts[s[i] - 'a']++;
    int64_t total = 0;
    for (int c = 0; c < 26; c++) total += counts[c] * (counts[c] + 1) / 2;
    return total;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    char *text = malloc(1000000);
    for (int64_t i = 0; i < 1000000; i++) {
        int64_t at = next_random() % 26;
        at = at * (next_random() % 26) / 25;
        text[i] = letters[at];
    }
    int64_t total = 0, check = 0;
    for (int k = 0; k < 5000; k++) {
        int64_t from = next_random() * 32768;
        from = (from + next_random()) % 900001;
        int64_t a = number_of_substrings(text + from, 100000);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    free(text);
    printf("5000 windows: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
