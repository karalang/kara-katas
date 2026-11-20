// LeetCode #2268: Minimum Number of Keypresses -- the bench, the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int by_largest(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x < y) - (x > y);
}

static int64_t minimum_keypresses(const char *s, int64_t n) {
    int64_t *count = calloc(26, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[s[i] - 'a']++;
    qsort(count, 26, sizeof(int64_t), by_largest);
    int64_t total = 0;
    for (int64_t i = 0; i < 26; i++) total += count[i] * (i / 9 + 1);
    free(count);
    return total;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2268;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t ks[] = {3, 10, 12, 26};
    char *s = malloc(100000);
    int64_t check = 0;
    for (int t = 0; t < 40; t++) {
        int64_t k = ks[t % 4];
        for (int i = 0; i < 100000; i++) s[i] = (char)('a' + next_random() % k);
        check = (check * 31 + minimum_keypresses(s, 100000)) % 1000000007;
    }
    free(s);
    printf("40 strings of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
