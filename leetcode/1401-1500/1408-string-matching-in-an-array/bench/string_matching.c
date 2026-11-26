// LeetCode #1408 bench, C: the same check of every word against every
// other, workload and checksum as string_matching.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define POOL 10000
#define WINDOW 100

static char pool[POOL][13];

int main(void) {
    int64_t seed = 1408;
    for (int i = 0; i < POOL; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int size = (int)(1 + seed / 65536 % 12);
        for (int k = 0; k < size; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            pool[i][k] = (char)('a' + seed / 65536 % 3);
        }
        pool[i][size] = 0;
    }
    int64_t check = 0;
    const char *words[WINDOW];
    for (int64_t r = 0; r < 2000; r++) {
        int64_t at = (check + r * 7919) % 9901;
        int n = 0;
        for (int i = 0; i < WINDOW; i++) {
            const char *w = pool[at + i];
            int seen = 0;
            for (int j = 0; j < n && !seen; j++) {
                seen = strcmp(words[j], w) == 0;
            }
            if (!seen) {
                words[n++] = w;
            }
        }
        int64_t found = 0, letters = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (strcmp(words[j], words[i]) != 0 && strstr(words[j], words[i]) != NULL) {
                    found++;
                    letters += (int64_t)strlen(words[i]);
                    break;
                }
            }
        }
        check = (check * 131 + found * 1000 + letters) % 1000000007;
    }
    printf("2000 windows of 100 words: checksum %lld\n", (long long)check);
    return 0;
}
