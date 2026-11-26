// LeetCode #1784: Check if Binary String Has at Most One Segment of Ones --
// the bench in C, mirroring check_ones_segment.kara: a search for "01".
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static bool check_ones_segment(const char *s) {
    return strstr(s, "01") == NULL;
}

static int64_t seed = 1784;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char strings[4000][101];
    for (int k = 0; k < 4000; k++) {
        int64_t ones = 1 + next_random() % 100;
        for (int i = 0; i < 100; i++) strings[k][i] = i < ones ? '1' : '0';
        strings[k][100] = 0;
        if (k % 2 == 1 && ones < 100) {
            int64_t at = ones + next_random() % (100 - ones);
            strings[k][at] = '1';
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 4000000; call++) {
        const char *s = strings[(check + call) % 4000];
        check = (check * 31 + (check_ones_segment(s) ? 2 : 1)) % 1000000007;
    }
    printf("4000000 calls over 4000 strings: checksum %lld\n", (long long)check);
    return 0;
}
