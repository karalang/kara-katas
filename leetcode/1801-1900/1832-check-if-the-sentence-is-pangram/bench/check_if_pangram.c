// LeetCode #1832: Check if the Sentence Is Pangram -- the bench in C: the ★
// arm over 100000 calls on runs of 500 to 999 letters cut from one string of
// 2000 letters, built once, each letter a z one time in 600 and otherwise one
// of a to y; each run's start and length are drawn from the checksum so far.
// Each call makes its run a string of its own.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool check_if_pangram(const char *sentence, int64_t n) {
    int64_t seen = 0;
    for (int64_t i = 0; i < n; i++) seen |= (int64_t)1 << (sentence[i] - 'a');
    return seen == ((int64_t)1 << 26) - 1;
}

static int64_t seed = 1832;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    char letters[2000];
    for (int i = 0; i < 2000; i++) {
        if (next_random() % 600 == 0) letters[i] = 'z';
        else letters[i] = (char)('a' + next_random() % 25);
    }
    int64_t check = 0, pangrams = 0;
    for (int64_t call = 0; call < 100000; call++) {
        int64_t start = (check + call) % 1000;
        int64_t len = 500 + (check * 7 + call) % 500;
        char *s = malloc((size_t)len + 1);
        memcpy(s, letters + start, (size_t)len);
        s[len] = 0;
        bool yes = check_if_pangram(s, len);
        free(s);
        if (yes) pangrams++;
        check = (check * 31 + (yes ? 2 : 1)) % 1000000007;
    }
    printf("100000 calls: %lld pangrams, checksum %lld\n", (long long)pangrams, (long long)check);
    return 0;
}
