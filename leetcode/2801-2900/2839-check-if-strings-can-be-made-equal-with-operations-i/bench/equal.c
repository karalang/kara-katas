// LeetCode #2839: Check if Strings Can be Made Equal With Operations I --
// the bench, mirrored from equal.kara: the even pair and the odd pair,
// each either way round.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int pair(char x, char y, char p, char q) { return (x == p && y == q) || (x == q && y == p); }

static int can_be_equal(const char *a, const char *b) {
    return pair(a[0], a[2], b[0], b[2]) && pair(a[1], a[3], b[1], b[3]);
}

int main(void) {
    const int64_t count = 1000000, rounds = 20;
    int64_t seed = 2839;
    char *words = malloc((size_t)count * 10);
    for (int64_t c = 0; c < count; c++) {
        char *a = words + c * 10, *b = a + 5;
        for (int i = 0; i < 4; i++) a[i] = (char)(97 + next_random(&seed) % 4);
        a[4] = 0;
        if (next_random(&seed) % 2 == 0) {
            memcpy(b, a, 5);
            char t = b[0]; b[0] = b[2]; b[2] = t;
        } else {
            for (int i = 0; i < 4; i++) b[i] = (char)(97 + next_random(&seed) % 4);
            b[4] = 0;
        }
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int same = can_be_equal(words + c * 10, words + c * 10 + 5);
            yes += same;
            check = (check * 31 + (same ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%lld pairs, %lld rounds: %lld true, checksum %lld\n", (long long)count, (long long)rounds, (long long)yes, (long long)check);
    free(words);
    return 0;
}
