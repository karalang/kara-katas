// Benchmark for #389: mirror of find_the_difference.kara (XOR of every byte).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static char find_the_difference(const char *s, int64_t m, const char *t, int64_t n) {
    uint8_t x = 0;
    for (int64_t i = 0; i < m; i++) x ^= (uint8_t)s[i];
    for (int64_t i = 0; i < n; i++) x ^= (uint8_t)t[i];
    return (char)x;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 389;
    char *pool = malloc(1000000);
    for (int i = 0; i < 1000000; i++) pool[i] = (char)(step(&seed) % 26 + 97);
    int64_t right = 0, checksum = 0;
    for (int64_t q = 0; q < 8000000; q++) {
        int64_t len = step(&seed) % 1001;
        int64_t a = step(&seed) % (1000000 - len - 1);
        char c = find_the_difference(pool + a, len, pool + a, len + 1);
        if (c == pool[a + len]) right++;
        checksum = (checksum * 31 + c) % 1000000007;
    }
    printf("8000000 pairs, %lld right, checksum %lld\n", (long long)right, (long long)checksum);
    free(pool);
    return 0;
}
