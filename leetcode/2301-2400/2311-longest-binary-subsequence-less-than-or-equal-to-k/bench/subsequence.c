// LeetCode #2311: Longest Binary Subsequence Less Than or Equal to K --
// the bench, the ★ arm in C. Greedy from the right: every 0 taken, and a
// 1 taken when its place still leaves the value at most k.
#include <stdint.h>
#include <stdio.h>

enum { STRINGS = 1000, LEN = 1000 };

static int64_t longest_subsequence(const char *s, int64_t n, int64_t k) {
    int64_t value = 0, taken = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        if (s[i] == '0')
            taken++;
        else if (taken < 31 && value + ((int64_t)1 << taken) <= k) {
            value += (int64_t)1 << taken;
            taken++;
        }
    }
    return taken;
}

static int64_t seed = 2311;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char strings[STRINGS][LEN];
    for (int a = 0; a < STRINGS; a++) {
        int64_t odds = next_random() % 8 + 1;
        for (int i = 0; i < LEN; i++) strings[a][i] = next_random() % odds == 0 ? '1' : '0';
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++)
        for (int64_t a = 0; a < STRINGS; a++)
            check = (check * 31 + longest_subsequence(strings[a], LEN, 10000000 * (p + 1) + a)) % 1000000007;
    printf("100 passes over 1000 strings of 1000 bits: checksum %lld\n", (long long)check);
    return 0;
}
