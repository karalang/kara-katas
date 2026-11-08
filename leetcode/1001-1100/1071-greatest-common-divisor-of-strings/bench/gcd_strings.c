// LeetCode #1071: Greatest Common Divisor of Strings -- the benchmark's C
// mirror of gcd_strings.kara: the same concatenations compared over 20000
// pairs built once, each answered 50 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *s;
    int64_t n;
} str;

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

// The answer as a new string: the two concatenations built and compared,
// then the prefix as long as the gcd of the lengths.
static str gcd_of_strings(str a, str b) {
    int64_t n = a.n + b.n;
    char *ab = malloc(n), *ba = malloc(n);
    memcpy(ab, a.s, a.n);
    memcpy(ab + a.n, b.s, b.n);
    memcpy(ba, b.s, b.n);
    memcpy(ba + b.n, a.s, a.n);
    int same = memcmp(ab, ba, n) == 0;
    free(ab);
    free(ba);
    str x = {malloc(1), 0};
    if (!same) {
        return x;
    }
    x.n = gcd(a.n, b.n);
    x.s = realloc(x.s, x.n);
    memcpy(x.s, a.s, x.n);
    return x;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static str random_word(int64_t n, int64_t k, int64_t *seed) {
    str s = {malloc(n), n};
    for (int64_t i = 0; i < n; i++) {
        s.s[i] = (char)('A' + next_random(seed) % k);
    }
    return s;
}

static str repeat(str r, int64_t times) {
    str s = {malloc(r.n * times), r.n * times};
    for (int64_t i = 0; i < times; i++) {
        memcpy(s.s + i * r.n, r.s, r.n);
    }
    return s;
}

#define N 20000

int main(void) {
    int64_t seed = 1071;
    static str as[N], bs[N];
    for (int i = 0; i < N; i++) {
        int64_t k = next_random(&seed) % 4 + 1;
        str root = random_word(next_random(&seed) % 20 + 1, k, &seed);
        str a = repeat(root, next_random(&seed) % 50 + 1);
        str b = repeat(root, next_random(&seed) % 50 + 1);
        free(root.s);
        int64_t roll = next_random(&seed) % 6;
        if (roll < 2) {
            int64_t at = next_random(&seed) % b.n;
            b.s[at] = (char)('A' + next_random(&seed) % k);
        } else if (roll == 2) {
            free(b.s);
            b = random_word(next_random(&seed) % 1000 + 1, k, &seed);
        }
        as[i] = a;
        bs[i] = b;
    }
    int64_t found = 0, letters = 0, check = 0;
    for (int r = 0; r < 50; r++) {
        for (int i = 0; i < N; i++) {
            str x = gcd_of_strings(as[i], bs[i]);
            if (x.n > 0) {
                found += 1;
            }
            letters += x.n;
            check = (check * 31 + x.n) % 1000000007;
            free(x.s);
        }
    }
    printf("1000000 calls: %lld found, %lld letters, checksum %lld\n", (long long)found, (long long)letters, (long long)check);
    return 0;
}
