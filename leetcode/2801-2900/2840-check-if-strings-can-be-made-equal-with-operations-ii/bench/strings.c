// LeetCode #2840: Check if Strings Can be Made Equal With Operations II
// -- the bench, mirrored from strings.kara: counts in one table of
// 2 x 26, s1 up and s2 down.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool check_strings(const char *s1, const char *s2, long n) {
    int64_t count[52] = {0};
    for (long i = 0; i < n; i++) {
        long side = i % 2 * 26;
        count[side + (s1[i] - 'a')] += 1;
        count[side + (s2[i] - 'a')] -= 1;
    }
    for (int k = 0; k < 52; k++)
        if (count[k] != 0) return false;
    return true;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 200, n = 100000, rounds = 20;
    int64_t seed = 2840;
    char **as = malloc(count * sizeof(char *));
    char **bs = malloc(count * sizeof(char *));
    for (long c = 0; c < count; c++) {
        char *a = malloc(n + 1), *b = malloc(n + 1);
        for (long i = 0; i < n; i++) a[i] = (char)(97 + next_random(&seed) % 26);
        a[n] = 0;
        memcpy(b, a, n + 1);
        for (long i = n - 1; i >= 2; i--) {
            long j = i % 2 + 2 * (next_random(&seed) % (i / 2 + 1));
            if (j <= i) {
                char t = b[i];
                b[i] = b[j];
                b[j] = t;
            }
        }
        if (c % 2 == 1) {
            long k = next_random(&seed) % n;
            b[k] = (char)(97 + next_random(&seed) % 26);
        }
        as[c] = a;
        bs[c] = b;
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            bool same = check_strings(as[c], bs[c], n);
            if (same) yes++;
            check = (check * 31 + (same ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%ld pairs of %ld, %ld rounds: %lld true, checksum %lld\n", count, n, rounds, (long long)yes, (long long)check);
    for (long c = 0; c < count; c++) {
        free(as[c]);
        free(bs[c]);
    }
    free(as);
    free(bs);
    return 0;
}
