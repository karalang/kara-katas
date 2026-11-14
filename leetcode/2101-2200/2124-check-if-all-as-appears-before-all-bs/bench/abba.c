// LeetCode #2124: Check if All A's Appears Before All B's -- the
// benchmark, the same algorithm as abba.kara: the answer is that "ba"
// does not occur, found with strstr.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int check_string(const char *s) {
    return strstr(s, "ba") == NULL;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char strings[100000][101];

int main(void) {
    int64_t seed = 2124;
    for (int n = 0; n < 100000; n++) {
        int64_t split = next_random(&seed) % 101;
        for (int i = 0; i < 100; i++) strings[n][i] = i < split ? 'a' : 'b';
        strings[n][100] = 0;
        if (next_random(&seed) % 4 == 0) {
            int64_t at = next_random(&seed) % 100;
            strings[n][at] = strings[n][at] == 'a' ? 'b' : 'a';
        }
    }
    int64_t ordered = 0, check = 0;
    for (int round = 0; round < 50; round++) {
        int k = round * 7919 % 100000, at = round * 31 % 100;
        strings[k][at] = strings[k][at] == 'a' ? 'b' : 'a';
        for (int i = 0; i < 100000; i++) {
            if (check_string(strings[i])) {
                ordered++;
                check = (check * 31 + i) % 1000000007;
            }
        }
    }
    printf("5000000 checks: %lld in order, checksum %lld\n", (long long)ordered, (long long)check);
    return 0;
}
