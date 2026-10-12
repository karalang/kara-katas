// Benchmark for #383: mirror of ransom_note.kara (26 letter counts).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int can_construct(const char *note, int64_t n, const char *mag, int64_t m) {
    int64_t count[26] = {0};
    for (int64_t i = 0; i < m; i++) count[mag[i] - 'a']++;
    for (int64_t i = 0; i < n; i++)
        if (--count[note[i] - 'a'] < 0) return 0;
    return 1;
}

int main(void) {
    int64_t seed = 383;
    char *pool = malloc(1000000);
    for (int i = 0; i < 1000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        pool[i] = (char)((seed / 65536) % 26 + 97);
    }
    int64_t yes = 0, checksum = 0;
    for (int q = 0; q < 10000; q++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t n = 30000 + (seed / 64) % 40000;
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t m = 40000 + (seed / 64) % 40000;
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t a = (seed / 64) % (1000000 - n);
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t b = (seed / 64) % (1000000 - m);
        int ok = can_construct(pool + a, n, pool + b, m);
        yes += ok;
        checksum = (checksum * 3 + (ok ? 1 : 2)) % 1000000007;
    }
    printf("%lld of 10000 can be built, checksum %lld\n", (long long)yes, (long long)checksum);
    free(pool);
    return 0;
}
