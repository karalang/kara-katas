// LeetCode #1576: Replace All ?'s to Avoid Consecutive Repeating
// Characters -- bench: the ★ arm (the first of a, b, c that fits, in a
// Vec[char]) over 20 strings of 500000 characters, half of them '?', built
// once; then 4 rounds answering all 20, each answer folded to its count of
// 'a's.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// The answer in a new buffer, as the other languages build a new string.
static char *modify_string(const char *s, int64_t n) {
    char *cs = malloc(n + 1);
    memcpy(cs, s, n + 1);
    const char letters[3] = {'a', 'b', 'c'};
    for (int64_t i = 0; i < n; i++) {
        if (cs[i] == '?') {
            for (int k = 0; k < 3; k++) {
                char c = letters[k];
                if ((i == 0 || cs[i - 1] != c) && (i + 1 == n || cs[i + 1] != c)) {
                    cs[i] = c;
                    break;
                }
            }
        }
    }
    return cs;
}

static int64_t seed = 1576;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t n = 500000;
    char *strings[20];
    for (int v = 0; v < 20; v++) {
        char *s = malloc(n + 1);
        char last = ' ';
        for (int64_t i = 0; i < n; i++) {
            if (next_random() % 2 == 0) {
                s[i] = '?';
                last = '?';
            } else {
                int64_t k = next_random() % 26;
                if ((char)('a' + k) == last) {
                    k = (k + 1) % 26;
                }
                s[i] = (char)('a' + k);
                last = s[i];
            }
        }
        s[n] = 0;
        strings[v] = s;
    }
    int64_t check = 0, total = 0;
    for (int r = 0; r < 4; r++) {
        for (int v = 0; v < 20; v++) {
            char *out = modify_string(strings[v], n);
            int64_t a = 0;
            for (int64_t i = 0; i < n; i++) {
                a += out[i] == 'a';
            }
            free(out);
            total += a;
            check = mix(check, a);
        }
    }
    printf("80 answers over 20 strings of %lld characters: 'a' total %lld, checksum %lld\n", (long long)n,
           (long long)total, (long long)check);
    for (int v = 0; v < 20; v++) {
        free(strings[v]);
    }
    return 0;
}
