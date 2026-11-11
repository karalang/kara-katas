// LeetCode #2116: Check if a Parentheses String Can Be Valid -- the
// benchmark, the same algorithm as valid.kara: two greedy passes over the
// bytes.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool can_be_valid(const char *s, const char *locked, int64_t n) {
    if (n % 2 == 1) {
        return false;
    }
    int64_t open = 0;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == '(' || locked[i] == '0') {
            open++;
        } else {
            open--;
            if (open < 0) {
                return false;
            }
        }
    }
    int64_t close = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        if (s[i] == ')' || locked[i] == '0') {
            close++;
        } else {
            close--;
            if (close < 0) {
                return false;
            }
        }
    }
    return true;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2116;
    const int64_t n = 50000;
    const int64_t cap = n + 2 * 40;
    char *strings[64];
    char *locks[64];
    int64_t len[64];
    for (int k = 0; k < 64; k++) {
        int64_t flip = next_random(&seed) % 2 == 0 ? next_random(&seed) % n : -1;
        strings[k] = malloc(cap);
        locks[k] = malloc(cap);
        int64_t open = 0;
        for (int64_t i = 0; i < n; i++) {
            bool up;
            if (open == 0) {
                up = true;
            } else if (open == n - i) {
                up = false;
            } else {
                up = next_random(&seed) % 2 == 0;
            }
            open += up ? 1 : -1;
            if (i == flip) {
                up = !up;
            }
            strings[k][i] = up ? '(' : ')';
            bool unlocked = next_random(&seed) % 4 == 0 && k % 2 == 0;
            locks[k][i] = unlocked ? '0' : '1';
        }
        len[k] = n;
    }
    int64_t valid = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 40; round++) {
        for (int a = 0; a < 64; a++) {
            strings[a][len[a]] = '(';
            strings[a][len[a] + 1] = ')';
            locks[a][len[a]] = '1';
            locks[a][len[a] + 1] = '1';
            len[a] += 2;
            bool got = can_be_valid(strings[a], locks[a], len[a]);
            if (got) {
                valid++;
            }
            check = (check * 31 + (got ? round + a : 1)) % 1000000007;
        }
    }
    printf("2560 solves: %lld can be valid, checksum %lld\n", (long long)valid, (long long)check);
    for (int k = 0; k < 64; k++) {
        free(strings[k]);
        free(locks[k]);
    }
    return 0;
}
