#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_byte(const void *x, const void *y) {
    return (int)*(const unsigned char *)x - (int)*(const unsigned char *)y;
}

/* Each string's letters copied into a fresh array and sorted, as the Kara
   arm sorts a Vec of its bytes. */
static bool check_if_can_break(const char *s1, const char *s2, size_t n) {
    unsigned char *a = malloc(n), *b = malloc(n);
    memcpy(a, s1, n);
    memcpy(b, s2, n);
    qsort(a, n, 1, by_byte);
    qsort(b, n, 1, by_byte);
    bool up = true, down = true;
    for (size_t i = 0; i < n && up; i++) up = a[i] >= b[i];
    for (size_t i = 0; i < n && down; i++) down = a[i] <= b[i];
    free(a);
    free(b);
    return up || down;
}

int main(void) {
    int64_t seed = 1433;
    char *pool = malloc(1000000), *up = malloc(1000000);
    for (int i = 0; i < 1000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        char c = (char)('a' + seed / 65536 % 25);
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool[i] = c;
        up[i] = (char)(c + seed / 65536 % 2);
    }
    int64_t breaks = 0;
    for (int i = 0; i < 400; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t one = (high * 32768 + seed / 65536) % 900001;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        bool got;
        if (seed / 65536 % 2 == 0) {
            got = check_if_can_break(pool + one, up + one, 100000);
        } else {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t two = (high * 32768 + seed / 65536) % 900001;
            got = check_if_can_break(pool + one, pool + two, 100000);
        }
        if (got) breaks++;
    }
    printf("400 pairs of 10^5 letters: %lld can break\n", (long long)breaks);
    free(pool);
    free(up);
    return 0;
}
