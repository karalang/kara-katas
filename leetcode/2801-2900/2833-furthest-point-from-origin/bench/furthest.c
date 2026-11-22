// LeetCode #2833: Furthest Point From Origin -- the bench, mirrored from
// furthest.kara: the L and R counts, and the blanks.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t furthest_distance_from_origin(const char *moves) {
    int64_t len = (int64_t)strlen(moves), left = 0, right = 0;
    for (int64_t i = 0; i < len; i++) left += moves[i] == 'L';
    for (int64_t i = 0; i < len; i++) right += moves[i] == 'R';
    int64_t gap = left - right;
    return (gap < 0 ? -gap : gap) + len - left - right;
}

int main(void) {
    const int64_t count = 100000, rounds = 100, n = 50;
    int64_t seed = 2833;
    char *strings = malloc((size_t)(count * (n + 1)));
    for (int64_t c = 0; c < count; c++) {
        int64_t blank = next_random(&seed) % 6;
        char *s = strings + c * (n + 1);
        for (int64_t i = 0; i < n; i++) {
            int64_t r = next_random(&seed) % 6;
            s[i] = r < blank ? '_' : (r % 2 == 0 ? 'L' : 'R');
        }
        s[n] = 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t d = furthest_distance_from_origin(strings + c * (n + 1));
            total += d;
            check = (check * 31 + d + r) % 1000000007;
        }
    }
    printf("%lld strings of %lld, %lld rounds: distances total %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(strings);
    return 0;
}
