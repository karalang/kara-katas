// LeetCode #2802: Find The K-th Lucky Number -- the bench in C: the ★ arm
// over 200000 k up to 10^9, all drawn first, then each answered 10 times;
// the answer written into a heap buffer, as the other languages allocate
// a string.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 200000

static int64_t seed = 2802;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static char *kth_lucky_number(int64_t k) {
    int64_t n = k + 1, top = 1;
    while (top * 2 <= n) top *= 2;
    char *lucky = malloc(64);
    size_t len = 0;
    for (int64_t bit = top / 2; bit > 0; bit /= 2) lucky[len++] = (n & bit) == 0 ? '4' : '7';
    lucky[len] = 0;
    return lucky;
}

static int64_t digest(const char *s) {
    int64_t h = 0;
    for (; *s; s++) h = (h * 131 + (unsigned char)*s) % 1000000007;
    return h;
}

static int64_t ks[COUNT];

int main(void) {
    int rounds = 10;
    for (int i = 0; i < COUNT; i++) ks[i] = wide() % 1000000000 + 1;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            char *s = kth_lucky_number(ks[i]);
            total += (int64_t)strlen(s);
            check = (check * 31 + digest(s) + r) % 1000000007;
            free(s);
        }
    }
    printf("%d k up to 10^9, %d rounds: lengths sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
