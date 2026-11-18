// LeetCode #2266: Count Number of Texts -- C mirror of the ★ arm
// (texts.kara): ways[i] adds ways[i - j] for each run of j equal presses
// ending at i, up to 3, or 4 on `7` and `9`, the table malloc'd per
// call. Output is byte-identical to texts.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL

static int64_t count_texts(const char *keys, int n) {
    int64_t *ways = calloc(n + 1, sizeof(int64_t));
    ways[0] = 1;
    for (int i = 1; i <= n; i++) {
        char key = keys[i - 1];
        int most = key == '7' || key == '9' ? 4 : 3;
        for (int j = 1; j <= most && j <= i && keys[i - j] == key; j++) {
            ways[i] = (ways[i] + ways[i - j]) % MOD;
        }
    }
    int64_t answer = ways[n];
    free(ways);
    return answer;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2266;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *sets[] = {"2", "79", "234", "23456789"};
    char *pressed = malloc(100000);
    int64_t check = 0;
    for (int t = 0; t < 40; t++) {
        const char *keys = sets[t % 4];
        int64_t len = (int64_t)strlen(keys);
        for (int i = 0; i < 100000; i++) pressed[i] = keys[next_random() % len];
        check = (check * 31 + count_texts(pressed, 100000)) % 1000000007;
    }
    free(pressed);
    printf("40 strings of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
