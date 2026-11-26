// LeetCode #1415 bench, C: the first letter from (k - 1) / 2^(n - 1), and
// each letter after it the lower or the higher of the two that differ from
// the one before, workload and checksum as get_happy_string.kara. The
// string and the two options are heap buffers, as Kāra's `String` and
// `Vec` are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static char *get_happy_string(int32_t n, int32_t k, size_t *len) {
    int32_t per_first = 1 << (n - 1);
    char *s = malloc(16);
    *len = 0;
    if (k > 3 * per_first) {
        return s;
    }
    const char letters[3] = {'a', 'b', 'c'};
    int32_t rest = k - 1;
    char last = letters[rest / per_first];
    rest %= per_first;
    s[(*len)++] = last;
    for (int32_t bit = per_first / 2; bit > 0; bit /= 2) {
        char *options = malloc(3);
        int m = 0;
        for (int i = 0; i < 3; i++) {
            if (letters[i] != last) {
                options[m++] = letters[i];
            }
        }
        last = options[rest >= bit ? 1 : 0];
        free(options);
        if (rest >= bit) {
            rest -= bit;
        }
        s[(*len)++] = last;
    }
    return s;
}

int main(void) {
    int64_t seed = 1415, check = 0;
    for (int r = 0; r < 1000000; r++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t n = 1 + seed / 65536 % 10;
        int64_t k = 1 + seed / 1024 % 100;
        size_t len;
        char *s = get_happy_string((int32_t)n, (int32_t)k, &len);
        int64_t sum = 0;
        for (size_t i = 0; i < len; i++) {
            sum = sum * 3 + (unsigned char)s[i];
        }
        free(s);
        check = (check * 131 + sum + (int64_t)len) % 1000000007;
    }
    printf("10^6 cases: checksum %lld\n", (long long)check);
    return 0;
}
