// LeetCode #2315: Count Asterisks -- the bench, the ★ arm in C. One pass
// with a flag: each `|` flips whether the walk is inside a pair, and a
// `*` counts only outside one.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

enum { STRINGS = 1000, LEN = 1000 };

static int64_t count_asterisks(const char *s, int64_t n) {
    bool inside = false;
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == '|')
            inside = !inside;
        else if (s[i] == '*' && !inside)
            count++;
    }
    return count;
}

static int64_t seed = 2315;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char strings[STRINGS][LEN];
    for (int a = 0; a < STRINGS; a++) {
        int64_t bars = next_random() % 8 + 2;
        int count = 0;
        for (int i = 0; i < LEN - 1; i++) {
            if (next_random() % bars == 0) {
                strings[a][i] = '|';
                count++;
            } else if (next_random() % 2 == 0) {
                strings[a][i] = '*';
            } else {
                strings[a][i] = 'a';
            }
        }
        strings[a][LEN - 1] = count % 2 == 1 ? '|' : 'a';
    }
    int64_t check = 0;
    for (int p = 0; p < 100; p++)
        for (int a = 0; a < STRINGS; a++)
            check = (check * 31 + count_asterisks(strings[(7 * a + p) % STRINGS], LEN)) % 1000000007;
    printf("100 passes over 1000 strings of 1000 characters: checksum %lld\n", (long long)check);
    return 0;
}
