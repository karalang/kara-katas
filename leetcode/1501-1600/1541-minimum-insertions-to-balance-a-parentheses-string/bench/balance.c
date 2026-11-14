// LeetCode #1541: Minimum Insertions to Balance a Parentheses String --
// bench: the ★ arm (one pass keeping the ')' still wanted) over 100 strings
// of 1 to 100000 parentheses, built once, each asked 10 times. C mirror of
// balance.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_insertions(const char *s, int64_t n) {
    int64_t inserted = 0, need = 0;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == '(') {
            if (need % 2 == 1) {
                inserted += 1;
                need -= 1;
            }
            need += 2;
        } else {
            need -= 1;
            if (need < 0) {
                inserted += 1;
                need = 1;
            }
        }
    }
    return inserted + need;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1541;
    char *strings[100];
    int64_t lens[100];
    for (int k = 0; k < 100; k++) {
        int64_t a = next_random(&seed);
        int64_t n = (a * 32768 + next_random(&seed)) % 100000 + 1;
        int64_t chance = next_random(&seed) % 101;
        char *s = malloc(n);
        for (int64_t i = 0; i < n; i++) {
            s[i] = next_random(&seed) % 100 < chance ? '(' : ')';
        }
        strings[k] = s;
        lens[k] = n;
    }
    int64_t check = 0;
    for (int p = 0; p < 10; p++) {
        for (int k = 0; k < 100; k++) {
            check = mix(check, min_insertions(strings[k], lens[k]));
        }
    }
    for (int k = 0; k < 100; k++) {
        free(strings[k]);
    }
    printf("10 passes over 100 strings of up to 100000 parentheses: checksum %lld\n", (long long)check);
    return 0;
}
