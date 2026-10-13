// Benchmark for #482: C mirror of the ★ arm (back to front); see
// license_key_formatting.kara. The characters kept are written into a
// buffer back to front, which is then reversed into the key.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char *license_key_formatting(const char *s, long long n, long long k, long long *len) {
    char *backwards = malloc(2 * n + 1);
    long long out = 0, in_group = 0;
    for (long long i = n - 1; i >= 0; i--) {
        char c = s[i];
        if (c == '-') {
            continue;
        }
        if (in_group == k) {
            backwards[out++] = '-';
            in_group = 0;
        }
        backwards[out++] = (c >= 'a' && c <= 'z') ? (char)(c - 'a' + 'A') : c;
        in_group++;
    }
    char *key = malloc(out + 1);
    for (long long i = 0; i < out; i++) {
        key[i] = backwards[out - 1 - i];
    }
    key[out] = 0;
    free(backwards);
    *len = out;
    return key;
}

int main(void) {
    const char *alphabet = "abcxyzABCXYZ0189";
    long long seed = 482, n = 100000;
    char *s = malloc(n + 1);
    for (long long i = 0; i < n; i++) {
        if (next_random(&seed) % 4 == 0) {
            s[i] = '-';
        } else {
            s[i] = alphabet[next_random(&seed) % 16];
        }
    }
    s[n] = 0;
    long long total = 0, checksum = 0;
    for (long long k = 1; k <= 500; k++) {
        long long len;
        char *key = license_key_formatting(s, n, k, &len);
        total += len;
        checksum = (checksum * 31 + len * 7 + key[len / 2] + key[k]) % 1000000007;
        free(key);
    }
    printf("k = 1 to 500 on 100000 characters: keys add up to %lld characters, checksum %lld\n", total, checksum);
    free(s);
    return 0;
}
